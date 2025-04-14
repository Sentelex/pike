import src.graph_builder as gb
import src.state as st
from typing import Callable
import langgraph.graph as lgg
import langchain_core.messages as lcm
from fixtures import *
import langchain_core.tools as lcct
import unittest.mock


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
    full_state.full_messages = [lcm.BaseMessage(
        content=f"Test message {i}", type="text") for i in range(20)]
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
                id="tool-call-id-1"
            )
        ]
    )
    _graph = simple_graph(lambda s: gb.tools_node(s, tools=[test_tool]))
    updated_state = _graph.invoke(state)
    mock_tool.assert_called_once_with("value1", "value2")
    assert updated_state["messages"][-1].content.strip('"') == "value1 and value2"


def test_build_graph(mock_model):
    graph = gb.build_graph(model=mock_model, graph_id="default")
    pass
