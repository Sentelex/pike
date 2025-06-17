import pytest
import uuid as u
import fastapi.testclient as ft
import langchain_core.messages as lcm
import langchain_google_genai as lcg
import langchain_openai as loai
import src.mocks.mock_api_interfaces as mai
import src.chat as ct
import src.mocks.mock_model as mm
import src.mocks.backend_mocks as bm
import src.model as model
import pike as pike
import src.graph_builder as gb
from fixtures import agent_config


client = ft.TestClient(pike.api)


@pytest.fixture
def patch_chat_cache(monkeypatch):
    """
    Patch the global CHAT_CACHE to contain MOCK_CHAT_STORE for testing.
    """
    # Patch CHAT_CACHE to be a copy of MOCK_CHAT_STORE
    monkeypatch.setattr(ct, "CHAT_CACHE", bm.MOCK_CHAT_STORE.copy())
    yield


def ensure_unique_value(
    dict_with_id_list: list[dict], input_key: str = "ID"
) -> bool:
    id_set = set([datum[input_key] for datum in dict_with_id_list])
    return len(dict_with_id_list) == len(id_set)


def test_get_public_agents():
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert ensure_unique_value(data, "agentId")
    assert mai.mock_agent_interface() in data or mai.mock_agent_alt() in data


def test_get_user_info():
    mock_uinf = mai.mock_user_info()
    response = client.get(f"/user/{mock_uinf['userId']}")
    assert response.status_code == 200
    data = response.json()
    assert data == mock_uinf


def test_get_user_agents():
    mock_user_info = mai.mock_user_info()
    response = client.get(f"/user/{mock_user_info['userId']}/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert ensure_unique_value(data, "agentId")
    assert all("agentId" in agent for agent in data)


def test_get_user_chats():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    mock_chat_interface = mai.mock_chat_interface()
    response = client.get(
        f"/user/{mock_user_info['userId']}/agent/{mock_agent_interface['agentId']}/chats"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert ensure_unique_value(data, "chatId")
    assert any(chat["chatId"] == mock_chat_interface["chatId"]
               for chat in data)


def test_get_chat_history(patch_chat_cache):
    mock_chat = mai.mock_chat_interface()
    mock_chat_history = mai.mock_chat_history()
    response = client.get(f"/chat/{mock_chat['chatId']}/history")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert all(
        [
            data["messages"][i] == dict(mock_chat_history["messages"][i])
            for i in range(len(data["messages"]))
        ]
    )


def test_get_attachment():
    attachment = mai.mock_pdf_attachment()
    response = client.get("/attachment/0e3c04dd-268a-45d8-8834-fd0e3e0c9f47")
    assert response.status_code == 200
    assert response.json() == attachment


def test_get_agent():
    mock_agent_alt = mai.mock_agent_alt()
    response = client.get(f"/agent/{mock_agent_alt['agentId']}")
    assert response.status_code == 200
    data = response.json()
    assert data["agentId"] == mock_agent_alt["agentId"]


@pytest.mark.parametrize(("provider", "model"), [("google", "gemini-2.0-flash"), ("openai", "gpt-4o-mini")])
def test_create_agent(monkeypatch, provider, model, agent_config):
    agent_id = u.uuid4()
    agent_config["model"]["provider"] = provider
    agent_config["model"]["name"] = model
    # Post to the create_agent endpoint
    response = client.post(
        f"/create_agent/{agent_id}",
        json=agent_config
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["status"] == "success"
    assert data["agentId"] == str(agent_id)
    assert agent_id in gb.AGENT_CACHE
    assert gb.AGENT_CACHE[agent_id].model.name == model


def test_create_chat_default(monkeypatch):
    # Monkeypatch ChatGoogleGenerativeAI to use MockModel
    mock_response = mai.mock_chat_response()
    mock_model = mm.MockLLM(responses=[lcm.AIMessage(**mock_response)])
    monkeypatch.setattr(lcg, "ChatGoogleGenerativeAI", lambda *_args, **_kwargs: mock_model)
    monkeypatch.setattr(loai, "ChatOpenAI", lambda *_args, **_kwargs: mock_model)

    # Create chat without agent config (uses default)
    agent_id = u.uuid4()
    mock_user_info = mai.mock_user_info()
    chat_id = mai.mock_chat_alt()["chatId"]
    response = client.post(
        f"/user/{mock_user_info['userId']}/agent/{agent_id}/create_chat/{chat_id}",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    response = response.json()
    assert response["newChat"]["chatId"] == chat_id
    assert response["newChat"]["agentId"] == str(agent_id)
    assert response["newChat"]["isOpen"] is True
    assert response["newChat"]["isPinned"] is False
    assert response["newChat"]["isBookmarked"] is False
    assert response["message"]['content'] == mock_response['content']


def test_create_chat(monkeypatch, agent_config):
    # Monkeypatch each chat model to use MockModel
    mock_response = mai.mock_chat_response()
    mock_model = mm.MockLLM(responses=[lcm.AIMessage(**mock_response)])
    monkeypatch.setattr(lcg, "ChatGoogleGenerativeAI", lambda *_args, **_kwargs: mock_model)
    monkeypatch.setattr(loai, "ChatOpenAI", lambda *_args, **_kwargs: mock_model)

    agent_id = u.uuid4()
    # Post to the create_agent endpoint
    response = client.post(
        f"/create_agent/{agent_id}",
        json=agent_config
    )
    mock_user_info = mai.mock_user_info()
    chat_id = mai.mock_chat_alt()["chatId"]
    response = client.post(
        f"/user/{mock_user_info['userId']}/agent/{agent_id}/create_chat/{chat_id}",
        json={"message": "Hello"}
    )
    assert response.status_code == 200
    response = response.json()
    assert response["newChat"]["chatId"] == chat_id
    assert response["newChat"]["agentId"] == str(agent_id)
    assert response["newChat"]["isOpen"] is True
    assert response["newChat"]["isPinned"] is False
    assert response["newChat"]["isBookmarked"] is False
    assert response["message"]['content'] == mock_response['content']


def test_add_agent_to_user():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    response = client.post(
        f"/user/{mock_user_info['userId']}/agent/{mock_agent_interface['agentId']}/add"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert ensure_unique_value(data, "agentId")


def test_get_response(monkeypatch):
    # Monkeypatch both Google and OpenAI models to use MockModel
    mock_response = mai.mock_chat_response()
    mock_model = mm.MockLLM(responses=[lcm.AIMessage(**mock_response)])
    monkeypatch.setattr(lcg, "ChatGoogleGenerativeAI", lambda *_args, **_kwargs: mock_model)
    monkeypatch.setattr(loai, "ChatOpenAI", lambda *_args, **_kwargs: mock_model)

    chat = ct.Chat(
        messages=[],
        new_message=lcm.BaseMessage(content="Test message", type="text"),
        id=u.uuid4(),
        agent_id=u.uuid4()
    )
    chat_id = chat.id
    response = client.post(
        f"/chat/{chat_id}/response", json={"message": "Hello"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data['content'] == mock_response['content']


def test_remove_agent_from_user():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    response = client.delete(
        f"/user/{mock_user_info['userId']}/agent/{mock_agent_interface['agentId']}/delete"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert ensure_unique_value(data, "agentId")
    assert any(agent["agentId"] == mock_agent_interface["agentId"]
               for agent in data)


def test_remove_chat_from_user():
    mock_user_info = mai.mock_user_info()
    mock_chat = mai.mock_chat_interface()
    response = client.delete(
        f"/user/{mock_user_info['userId']}/chat/{mock_chat['chatId']}/delete"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert ensure_unique_value(data, "chatId")


def test_modify_chat_status(patch_chat_cache):
    mock_chat = mai.mock_chat_interface()
    chat_flags = {"pinned": True, "bookmarked": False, "opened": True}
    response = client.put(
        f"/chat/{mock_chat['chatId']}/status", json=chat_flags
    )
    assert response.status_code == 200
    data = response.json()
    assert data["isPinned"] is True
    assert data["isBookmarked"] is False
    assert data["isOpen"] is True
