import pytest
import langchain_core.messages as lcm
import uuid as u
import src.chat as ct
import src.graph_builder as gb


@pytest.fixture
def mock_message():
    """Fixture to provide a mock message."""
    return lcm.BaseMessage(content="Test message", type="text")


@pytest.fixture
def chat(mock_message):
    """Fixture to provide a mock chat."""
    return ct.Chat(
        messages=[],
        new_message=mock_message,
        id=u.uuid4(),
        agent_id=u.uuid4()
    )

@pytest.fixture
def agent_config():
    """Fixture to provide a mock agent config as a dict."""
    return {
        "name": "Test Agent",
        "description": "This is a test agent.",
        "model": {
            "name": "gemini-2.0-flash",
            "provider": "google",
            "api_key": "test_api_key",
            "additional_kwargs": {}
        },
        "tools": []
    }
