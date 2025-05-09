from fastapi.testclient import TestClient
import backend.src.mocks.mock_api_interfaces as mai
import backend.pike as pike

client = TestClient(pike.api)


def ensure_unique_value(
    dict_with_id_list: list[dict], input_key: str = "ID"
) -> bool:
    id_set = set([datum[input_key] for datum in dict_with_id_list])
    num_set = len(id_set)
    num_list = len(dict_with_id_list)
    q = num_set == num_list
    return q
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
    response = client.get(f"/user/{mock_uinf['agentId']}")
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
    assert any(chat["chatId"] == mock_chat_interface["chatId"] for chat in data)


def test_get_chat_history():
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


def test_create_chat():
    mock_user_info = mai.mock_user_info()
    mock_agent_interface = mai.mock_agent_interface()
    mock_chat_alt = mai.mock_chat_alt()
    response = client.post(
        f"/user/{mock_user_info['userId']}/agent/{mock_agent_interface['agentId']}/create_chat"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["chatId"] == mock_chat_alt["chatId"]


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


def test_get_response():
    chat_id = mai.mock_chat_interface()["chatId"]
    response = client.post(
        f"/chat/{chat_id}/response", json={"message": "Hello"})
    mock_response = mai.mock_chat_response()
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert all(
        [
            data["messages"][i] == dict(mock_response["messages"][i])
            for i in range(len(data["messages"]))
        ]
    )


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
    assert any(agent["agentId"] == mock_agent_interface["agentId"] for agent in data)


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


def test_modify_chat_status():
    mock_chat = mai.mock_chat_interface()
    chat_flags = {"pinned": True, "bookmarked": False, "open": True}
    response = client.put(
        f"/chat/{mock_chat['chatId']}/status", json={"chat_flags": chat_flags}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["pinned"] is True
    assert data["bookmarked"] is False
    assert data["open"] is True
