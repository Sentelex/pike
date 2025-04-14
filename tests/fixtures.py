import pytest
import langchain_core.messages as lcm
import src.state as st


@pytest.fixture
def mock_message():
    """Fixture to provide a mock message."""
    return lcm.BaseMessage(content="Test message", type="text")


@pytest.fixture
def mock_model():
    """Fixture to provide a mock model with a bind_tools() function."""
    class MockModel:
        def __init__(self):
            self.tools = []

        def bind_tools(self, tools):
            """Mock implementation of bind_tools."""
            self.tools = tools

    return MockModel()


@pytest.fixture
def full_state(mock_message):
    return st.StateFull(new_message=mock_message)


@pytest.fixture
def state(mock_message):
    return st.State(messages=[mock_message], new_message=mock_message)