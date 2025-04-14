import pytest
import src.graph_builder as gb
import src.state as st
from typing import Callable
import langgraph.graph as lgg
import langchain_core.messages as lcm
from fixtures import *


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
