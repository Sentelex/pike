import pytest as pytest
import pydantic as pdc
import langchain_core.messages as lcm
import langgraph.graph.message as lgm
import src.state as st
from tests.fixtures import *


def test_full_state_valid_data(mock_message):
    full_messages = [
        lcm.BaseMessage(content="Previous message 1", type="text"),
        lcm.BaseMessage(content="Previous message 2", type="text")
    ]
    state = st.StateFull(
        full_messages=full_messages,
        new_message=mock_message,
        attachment="example.pdf",
        graph_id="graph123"
    )
    assert state.full_messages == full_messages
    assert state.new_message == mock_message
    assert state.attachment == "example.pdf"
    assert state.graph_id == "graph123"


def test_state_missing_optional_fields(mock_message):
    state = st.StateFull(new_message=mock_message)
    assert state.full_messages == []
    assert state.attachment is None
    assert state.graph_id is None


def test_state_attributes(state):
    assert isinstance(state, st.State)
    assert isinstance(state.messages, list)
    assert isinstance(state.new_message, lcm.BaseMessage)
    assert isinstance(state.full_messages, list)
    assert state.attachment is None


def test_state_messages_missing(mock_message):
    with pytest.raises(pdc.ValidationError):
        st.State(new_message=mock_message)


def test_state_invalid_messages(mock_message):
    with pytest.raises(pdc.ValidationError):
        st.StateFull(
            full_messages="invalid_data", new_message=mock_message)


def test_state_invalid_attachment(mock_message):
    with pytest.raises(pdc.ValidationError):
        # attachment should be a string or None
        st.StateFull(new_message=mock_message, attachment=12345)
