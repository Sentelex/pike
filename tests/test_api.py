import pytest
from fastapi.testclient import TestClient
import backend.src.mock_api_interfaces as mai
import backend.pike as pike


client = TestClient(pike.api)


def test_get_public_agents():
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert mai.mock_agent_interface() in data or mai.mock_agent_alt() in data


def test_get_user_info():
    mock_uinf = mai.mock_user_info()
    response = client.get(f"/user/{mock_uinf['ID']}")
    assert response.status_code == 200
    data = response.json()
    assert data == mock_uinf


def test_get_user_agents():
    mock_user_info = mai.mock_user_info()
    response = client.get(f"/user/{mock_user_info['ID']}/agents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("ID" in agent for agent in data)


def test_get_user_chats():
    mock_user_info = mai.mock_user_info()
    mock_chat_interface = mai.mock_chat_interface()
    response = client.get(f"/user/{mock_user_info['ID']}/"
                          f"agent/{mock_user_info['agents'][0]['ID']}/chats")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or isinstance(data, tuple)
    assert any(chat["ID"] == mock_chat_interface["ID"] for chat in data)


def test_get_chat_history():
    mock_chat_history = mai.mock_chat_history()
    mock_chat = mai.mock_chat_interface()
    response = client.get(f"/chat/{mock_chat['ID']}")
    assert response.status_code == 200
    data = response.json()
    assert 'messages' in data
    assert all([data['messages'][i] == dict(mock_chat_history['messages'][i]) for i in range(len(data['messages']))])


def test_get_attachment():
    attachment = mai.mock_pdf_attachment()
    response = client.get("/attachment/0e3c04dd-268a-45d8-8834-fd0e3e0c9f47")
    assert response.status_code == 200
    assert response.json() == attachment


def test_get_agent():
    mock_agent_alt = mai.mock_agent_alt()
    response = client.get(f"/agent/{mock_agent_alt['ID']}")
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == mock_agent_alt["ID"]


def test_create_chat():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    mock_chat_alt = mai.mock_chat_alt()
    response = client.post(
        f"/user/{mock_user_info['ID']}/agent/{mock_agent_interface['ID']}/chat"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ID"] == mock_chat_alt["ID"]


def test_add_agent_to_user():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    response = client.post(
        f"/user/{mock_user_info['ID']}/agent/{mock_agent_interface['ID']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_response():
    chat_id = mai.mock_chat_interface()["ID"]
    response = client.post(
        f"/chat/{chat_id}", json={"message": "Hello"}
    )
    mock_response = mai.mock_chat_response()
    assert response.status_code == 200
    data = response.json()
    assert 'messages' in data
    assert all([data['messages'][i] == dict(mock_response['messages'][i]) for i in range(len(data['messages']))])



def test_remove_agent_from_user():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    response = client.delete(
        f"/user/{mock_user_info['ID']}/agent/{mock_agent_interface['ID']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(agent["ID"] == mock_agent_interface["ID"] for agent in data)


def test_remove_chat_from_user():
    mock_user_info = mai.mock_user_info()
    mock_chat = mai.mock_chat_interface()
    response = client.delete(f"/user/{mock_user_info['ID']}/chat/{mock_chat['ID']}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_modify_chat_status():
    mock_chat = mai.mock_chat_interface()
    chat_flags = {"pinned": True, "bookmarked": False, "open": True}
    response = client.put(
        f"/chat/{mock_chat['ID']}", json={"chat_flags": chat_flags}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["pinned"] is True
    assert data["bookmarked"] is False
    assert data["open"] is True
