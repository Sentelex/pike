import pytest
import langchain_core.messages as lcm
import backend.src.chat as ch
import uuid as u


@pytest.fixture
def mock_message():
    """Fixture to provide a mock message."""
    return lcm.BaseMessage(content="Test message", type="text")


@pytest.fixture
def chat(mock_message):
    return ch.Chat(
        messages=[],
        new_message=mock_message,
        id=u.uuid4(),
        agent_id=u.uuid4()
    )
