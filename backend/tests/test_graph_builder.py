import pytest
import src.graph_builder as gb
import src.state as st
from typing import Callable
import langgraph.graph as lgg
import langchain_core.messages as lcm
from tests.fixtures import *
import langchain_core.tools as lcct
import unittest.mock
import src.mocks.mock_model as mm
import os
import langchain_core.tools as lcct
import langchain_google_genai as lc_google
import dotenv


def simple_graph(node: Callable):
    graph_builder = lgg.StateGraph(st.State)
    graph_builder.add_node("test_node", node)
    graph_builder.add_edge(lgg.START, "test_node")
    graph_builder.add_edge("test_node", lgg.END)
    return graph_builder.compile()


def test_add_message_node(full_state):
    assert len(full_state.full_messages) == 0
    _graph = simple_graph(gb.add_new_message)
    updated_state = _graph.invoke(full_state)
    assert len(updated_state["full_messages"]) == 1
    assert updated_state["full_messages"][0] == full_state.new_message


def test_trunc_node(full_state):
    full_state.full_messages = [
        lcm.BaseMessage(content=f"Test message {i}", type="text") for i in range(20)
    ]
    assert len(full_state.full_messages) == 20
    _graph = simple_graph(gb.truncate_history)
    updated_state = _graph.invoke(full_state)
    assert len(updated_state["full_messages"]) == 20
    assert len(updated_state["messages"]) == 10


def test_tools_node(state):
    mock_tool = unittest.mock.MagicMock(return_value="value1 and value2")

    @lcct.tool
    def test_tool(arg1, arg2):
        """
        Mock tool that takes two arguments and returns a string.
        arg1: First argument
        arg2: Second argument
        Returns a string combining both arguments.
        """
        return mock_tool(arg1, arg2)

    # Add a valid message with the required 'role' and 'content' keys
    state.messages[-1] = lcm.AIMessage(
        content="Tool call executed",
        tool_calls=[
            lcm.ToolCall(
                name="test_tool",
                args={"arg1": "value1", "arg2": "value2"},
                id="tool-call-id-1",
            )
        ],
    )
    _graph = simple_graph(lambda s: gb.tools_node(s, tools=[test_tool]))
    updated_state = _graph.invoke(state)
    mock_tool.assert_called_once_with("value1", "value2")
    assert updated_state["messages"][-1].content.strip(
        '"') == "value1 and value2"


def test_build_graph_with_mocked_tools(state, monkeypatch):
    dummy_tool = unittest.mock.MagicMock()
    dummy_tool.name = "dummy_tool"
    dummy_tool.invoke = unittest.mock.MagicMock(
        return_value="result from dummy tool")

    # Patch the graph_builder to use only our dummy_tool for the 'default' graph
    monkeypatch.setitem(gb.TOOL_LIST_LOOKUP, "default", [dummy_tool])
    response_messages = [
        lcm.AIMessage(
            content="dummy input",
            tool_calls=[
                lcm.ToolCall(
                    name="dummy_tool",  # This must match the tool's name
                    args={"file_path": "dummy_path.pdf"},
                    id="tool-call-id-1",
                )
            ],
        ),
        lcm.AIMessage(content="tool call completed"),
    ]
    mock_model = mm.MockLLM(responses=response_messages)
    graph = gb.build_graph(model=mock_model, graph_id="default")
    updated_state = graph.invoke(state)
    dummy_tool.invoke.assert_called_once_with({"file_path": "dummy_path.pdf"})
    assert len(updated_state["messages"]) == 4
    assert updated_state["messages"][-2].content.strip(
        '"') == "result from dummy tool"


@pytest.mark.skip_in_pipeline
def test_gemini_model_calls_tool(monkeypatch):
    # Ensure API key is loaded
    dotenv.load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    assert api_key, "GOOGLE_API_KEY must be set in the environment"

    @lcct.tool
    def special_add(a: int, b: int) -> str:
        """A special add tool."""
        return a + 2 * b

    @lcct.tool
    def special_multiply(a: int, b: int) -> str:
        """A special multipy tool."""
        return a * b / 6

    monkeypatch.setitem(gb.TOOL_LIST_LOOKUP, "default",
                        [special_add, special_multiply])

    model = lc_google.ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", google_api_key=api_key
    )
    mock_message = lcm.HumanMessage(
        content="make a special addition of 2 and 5 and then special multiply by 4"
    )
    state = st.StateFull(new_message=mock_message)
    graph = gb.build_graph(model=model, graph_id="default")
    result_state = graph.invoke(state)
    assert len(result_state["messages"]) == 6
    assert isinstance(result_state["messages"][2], lcm.ToolMessage)
    assert isinstance(result_state["messages"][4], lcm.ToolMessage)
    assert "8" in result_state["messages"][-1].content
