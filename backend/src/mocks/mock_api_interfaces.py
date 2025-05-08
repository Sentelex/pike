import langchain_core.messages as lcm
import base64
import datetime as dt
import copy


def mock_model_interface():
    return {
        "model_name": "gpt-4o-mini",
        "api_key": "N0T-4-R34L-K3Y",
        "additonal_kwargs": {
            "temperature": 0.5,
            "max_tokens": 250
        },
    }


def mock_skill_interface():
    return {
        "ID": "8365d252-1bf2-46da-b621-5450e31eb90d",
        "name": "PDF Reader",
        "description": "Parses main-body text from PDFs",
    }


def mock_skill_alt():
    skill_alt = copy.copy(mock_skill_interface())
    skill_alt['ID'] = "d0e478dd-dd1b-4e55-9beb-ec6c2c3f18d7"
    skill_alt['name'] = "Image Reader"
    skill_alt['description'] = "Parses main-body text from images"
    skill_alt['model'] = mock_model_interface()
    return skill_alt


def mock_agent_interface():
    return {
        "agentId": "0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
        "agentName": "Default Agent 1",
        "developer": "PIKE",
        "description": "PIKE's default agent",
        "model": mock_model_interface(),
        "skills": [mock_skill_interface()],
    }


def mock_agent_alt():
    agent_alt = copy.copy(mock_agent_interface())
    agent_alt['skills'].append(mock_skill_alt())
    agent_alt['agentId'] = "bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48"
    agent_alt['agentName'] = "Default Agent 2"
    return agent_alt


def mock_jpeg_attachment():
    file_path = "bsckend/data/squeaky_bone.jpg"
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.urlsafe_b64encode(image_data).decode("utf-8")
    return encoded_image


def mock_pdf_attachment():
    file_path = "backend/data/dummy.pdf"
    with open(file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        encoded_pdf = base64.urlsafe_b64encode(pdf_data).decode("utf-8")
    return encoded_pdf


def mock_chat_interface():
    return {
        "chatId": "81bddc2b-36e6-495a-a8e4-d5207a50f121",
        "chatName": "First Chat - Agent 1",
        "isOpen": False,
        "isPinned": False,
        "isBookmarked": True,
        "to_delete": False,
        "created_at": dt.datetime(2023, 10, 4, 12, 0, 0),
        "updated_at": dt.datetime(2023, 10, 4, 12, 0, 0),
        "agentId": "0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
    }


def mock_chat_alt():
    return {
        "chatId": "cabddc2b-36e6-495a-a8e4-d5207a50f122",
        "chatName": "Second Chat - Agent 1",
        "isOpen": True,
        "isPinned": False,
        "isBookmarked": False,
        "created_at": dt.datetime(2023, 10, 4, 15, 0, 0),
        "updated_at": dt.datetime(2023, 10, 4, 15, 0, 0),
        "agentId": "0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
    }

def mock_chat_interface_2():
    return {
        "chatId": "81bddc2b-36e6-495a-a8e4-d5207a50f121",
        "chatName": "First Chat - Agent 2",
        "isOpen": False,
        "isPinned": False,
        "isBookmarked": True,
        "to_delete": False,
        "created_at": dt.datetime(2023, 10, 4, 12, 0, 0),
        "updated_at": dt.datetime(2023, 10, 4, 12, 0, 0),
        "agentId": "bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48",
    }


def mock_chat_alt_2():
    return {
        "chatId": "cabddc2b-36e6-495a-a8e4-d5207a50f122",
        "chatName": "Second Chat - Agent 2",
        "isOpen": True,
        "isPinned": False,
        "isBookmarked": False,
        "created_at": dt.datetime(2023, 10, 4, 15, 0, 0),
        "updated_at": dt.datetime(2023, 10, 4, 15, 0, 0),
        "agentId": "bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48",
    }


def mock_chat_history():
    return {
        "messages": [
            lcm.HumanMessage(
                content="This is a basic human input message to the chat."),
            lcm.AIMessage(
                content="This is an AI response to the human message."),
            lcm.HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": "Please find me something like this image.",
                    },
                    {
                        "type": "image",
                        "attachment_id": "d0e478dd-dd1b-4e55-9beb-ec6c2c3f18d7",
                    },
                ]
            ),
        ]
    }


def mock_chat_history_alt() -> dict:
    return {
        " messages": [
            lcm.HumanMessage(
                content="This is a basic human input message to the chat."),
            lcm.AIMessage(
                content="This is an AI response to the human message."),
            lcm.HumanMessage(
                content=[
                    {"type": "text", "text": "Summarize this document."},
                    {
                        "type": "pdf",
                        "attachment_id": "20a6737d-1fb6-4a63-9d9f-c0034d77153e",
                    },
                ]
            ),
        ]
    }


def mock_chat_response():
    return {
        "messages": [lcm.AIMessage(content="This is an AI response to the human message.")]
    }


def mock_user_info() -> dict:
    return {
        "userId": "6b96666e-8b3a-4996-932d-3aa75c08c16f",
        "userName": "Michael Luch",
        "userAgents": [mock_agent_interface(), mock_agent_alt()],
    }

def mock_pinned_chats_list() -> dict:
    return [
			{
				"chatId": 1,
				"agentId": 2,
				"chatName": 'Pinned Chat 1',
				"chatAgent": 'Personal Finance Manager',
			},
			{
				"chatId": 1,
				"agentId": 1,
				"chatName": 'Pinned Chat 2',
				"chatAgent": 'Document Assistant',
			},
			{
				"chatId": 2,
				"agentId": 2,
				"chatName": 'Pinned Chat 3',
				"chatAgent": 'Personal Finance Manager',
			},
		]