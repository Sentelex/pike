import pytest
from fastapi.testclient import TestClient
import backend.pike as pike

# Import fixtures from tests/api_fixtures.py
pytest_plugins = ["tests.api_fixtures"]

client = TestClient(pike.api)


def test_get_public_agents(mock_agent_one_skill, mock_agent_two_skills):
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert mock_agent_one_skill in data or mock_agent_two_skills in data


def test_get_user_info(mock_user):
    response = client.get(f"/user/{mock_user['ID']}")
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == mock_user["ID"]


def test_get_user_agents(mock_user):
    response = client.get(f"/user/{mock_user['ID']}/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("ID" in agent for agent in data)


def test_get_user_chats_compact(
    mock_chat_without_messages, mock_additional_chat_without_messages, mock_user
):
    response = client.get(f"/user/{mock_user['ID']}/chats")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or isinstance(data, tuple)
    assert any(chat["ID"] == mock_chat_without_messages["ID"] for chat in data)


def test_get_user_chats_by_agent(
    mock_chat_without_messages, mock_user, mock_agent_one_skill
):
    response = client.get(
        f"/user/{mock_user['ID']}/agent/{mock_agent_one_skill['ID']}/chats"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == mock_chat_without_messages["ID"]


def test_get_user_chat(mock_chat_with_messages, mock_user):
    chat_id = (
        mock_chat_with_messages["ID"]
        if "ID" in mock_chat_with_messages
        else "test-chat-id"
    )
    response = client.get(f"/user/{mock_user['ID']}/chat/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data


def test_get_attachment(mock_attachment_database):
    attachment_id = list(mock_attachment_database.keys())[0]
    response = client.get(f"/attachment/{attachment_id}")
    assert response.status_code == 200
    assert response.text.strip() != ""


def test_get_agent(mock_agent_two_skills):
    response = client.get(f"/agent/{mock_agent_two_skills['ID']}")
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == mock_agent_two_skills["ID"]


def test_create_chat(
    mock_user, mock_agent_one_skill, mock_additional_chat_without_messages
):
    response = client.post(
        f"/user/{mock_user['ID']}/agent/{mock_agent_one_skill['ID']}/chat"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == mock_additional_chat_without_messages["ID"]


def test_add_agent_to_user(mock_user, mock_agent_one_skill):
    response = client.post(
        f"/user/{mock_user['ID']}/agent/{mock_agent_one_skill['ID']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_invoke_chat(mock_user, mock_chat_with_messages):
    chat_id = (
        mock_chat_with_messages["ID"]
        if "ID" in mock_chat_with_messages
        else "test-chat-id"
    )
    response = client.post(
        f"/user/{mock_user['ID']}/chat/{chat_id}", json={"input": "Hello"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data or isinstance(data, list)


def test_remove_agent_from_user(mock_user, mock_agent_one_skill):
    response = client.delete(
        f"/user/{mock_user['ID']}/agent/{mock_agent_one_skill['ID']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(agent["ID"] == mock_agent_one_skill["ID"] for agent in data)


def test_remove_chat_from_user(mock_user, mock_chat_with_messages):
    chat_id = (
        mock_chat_with_messages["ID"]
        if "ID" in mock_chat_with_messages
        else "test-chat-id"
    )
    response = client.delete(f"/user/{mock_user['ID']}/chat/{chat_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_modify_chat_status(mock_user, mock_chat_with_messages):
    chat_id = (
        mock_chat_with_messages["ID"]
        if "ID" in mock_chat_with_messages
        else "test-chat-id"
    )
    chat_flags = {"pinned": True, "bookmarked": False, "open": True}
    response = client.put(
        f"/user/{mock_user['ID']}/chat/{chat_id}", json={"chat_flags": chat_flags}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["pinned"] is True
    assert data["bookmarked"] is False
    assert data["open"] is True
