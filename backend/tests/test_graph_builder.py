import pytest
import backend.src.graph_builder as gb
import backend.src.chat as ct
from typing import Callable
import langgraph.graph as lgg
import langchain_core.messages as lcm
from tests.fixtures import *
import langchain_core.tools as lcct
import unittest.mock
import src.mocks.mock_model as mm
import os
import langchain_core.tools as lcct
import langchain_google_genai as lcg
import dotenv
import uuid as u


def simple_graph(node: Callable):
    graph_builder = lgg.StateGraph(ct.Chat)
    graph_builder.add_node("test_node", node)
    graph_builder.add_edge(lgg.START, "test_node")
    graph_builder.add_edge("test_node", lgg.END)
    return graph_builder.compile()


def test_add_message_node(chat):
    assert len(chat.messages) == 0
    _graph = simple_graph(gb.add_new_message)
    updated_chat = _graph.invoke(chat)
    assert len(updated_chat["messages"]) == 1
    assert updated_chat["messages"][0] == chat.new_message


def test_tools_node(chat):
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
    chat.messages = [lcm.AIMessage(
        content="Tool call executed",
        tool_calls=[
            lcm.ToolCall(
                name="test_tool",
                args={"arg1": "value1", "arg2": "value2"},
                id="tool-call-id-1",
            )
        ],
    )]
    _graph = simple_graph(lambda s: gb.tools_node(s, tools=[test_tool]))
    updated_chat = _graph.invoke(chat)
    mock_tool.assert_called_once_with("value1", "value2")
    assert updated_chat["messages"][-1].content.strip(
        '"') == "value1 and value2"


def test_build_graph_with_mocked_tools(chat):
    dummy_tool = unittest.mock.MagicMock()
    dummy_tool.name = "dummy_tool"
    dummy_tool.invoke = unittest.mock.MagicMock(
        return_value="result from dummy tool")

    # Patch the graph_builder to use only our dummy_tool for the 'default' graph
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
    graph = gb.build_graph(model=mock_model, tools=[dummy_tool])
    updated_chat = graph.invoke(chat)
    dummy_tool.invoke.assert_called_once_with({"file_path": "dummy_path.pdf"})
    assert len(updated_chat["messages"]) == 4
    assert updated_chat["messages"][-2].content.strip(
        '"') == "result from dummy tool"
