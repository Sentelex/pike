import pytest
import backend.src.mocks.mock_model as mock
import langchain_core.messages as lc_messages


def test_mock_llm_single_response():
    llm = mock.MockLLM()
    response = llm.invoke("Hello")
    assert response.content == "This is a mock response."
    assert llm.call_count == 1


def test_mock_llm_multiple_responses():
    responses = ["Response 1", "Response 2", "Response 3"]
    llm = mock.MockLLM(responses=responses)
    for i in range(6):
        assert llm.invoke("Test").content == responses[i % 3]
    assert llm.call_count == 6


def test_mock_llm_with_message_list():
    llm = mock.MockLLM(["Mocked"])
    messages = [
        lc_messages.HumanMessage(content="Hello"),
        lc_messages.HumanMessage(content="World"),
    ]
    response = llm.invoke(messages)
    assert response.content == "Mocked"
    assert llm.call_count == 1


def test_mock_llm_invalid_input():
    llm = mock.MockLLM()
    with pytest.raises(ValueError):
        llm.invoke(42)  # Unsupported input type
