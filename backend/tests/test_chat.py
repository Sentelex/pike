import pytest as pytest
import pydantic as pdc
import langchain_core.messages as lcm
import langgraph.graph.message as lgm
import src.chat as ct
from tests.fixtures import *
import uuid as u


def test_chat_valid_data(mock_message):
    messages = [
        lcm.BaseMessage(content="Previous message 1", type="text"),
        lcm.BaseMessage(content="Previous message 2", type="text"),
    ]
    agent_id = u.uuid4()
    chat = ct.Chat(
        messages=messages,
        new_message=mock_message,
        id=u.uuid4(),
        agent_id=agent_id,
    )
    assert chat.messages == messages
    assert chat.new_message == mock_message
    assert chat.agent_id == agent_id


def test_chat_missing_optional_fields(mock_message):
    chat = ct.Chat(new_message=mock_message, id=u.uuid4(), agent_id=u.uuid4())
    assert chat.messages == []


def test_chat_attributes(chat):
    assert isinstance(chat.messages, list)
    assert isinstance(chat.new_message, lcm.BaseMessage)
    assert isinstance(chat.messages, list)


def test_chat_messages_missing(mock_message):
    with pytest.raises(pdc.ValidationError):
        ct.Chat(new_message=mock_message)


def test_chat_invalid_messages(mock_message):
    with pytest.raises(pdc.ValidationError):
        ct.Chat(messages="invalid_data", new_message=mock_message)


def test_chat_invalid_attachment(mock_message):
    with pytest.raises(pdc.ValidationError):
        # attachment should be a string or None
        ct.Chat(new_message=mock_message, attachment=12345)
        

