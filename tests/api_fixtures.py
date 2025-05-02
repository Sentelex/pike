import pytest
import langchain_core.messages as lcm
import base64
import datetime as dt
import copy

additional_kwargs = {"temperature": 0.5, "max_tokens": 250}


@pytest.fixture
def mock_additional_kwargs():
    """Fixture to provide a mock set of additional keyword arguments"""
    return additional_kwargs


model = {
    "model_name": "gpt-4o-mini",
    "api_key": "N0T-4-R34L-K3Y",
    "additonal_kwargs": additional_kwargs,
}


@pytest.fixture
def mock_model():
    return model


skill = {
    "ID": "8365d252-1bf2-46da-b621-5450e31eb90d",
    "name": "PDF Reader",
    "description": "Parses main-body text from PDFs",
}


@pytest.fixture
def mock_skill():
    return skill


skill_with_model = skill | {"model": model}


@pytest.fixture
def mock_skill_with_model():
    return skill_with_model


agent_one_skill = {
    "ID": "0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
    "name": "Default Agent",
    "description": "PIKE's default agent",
    "model": model,
    "skills": [skill],
}


@pytest.fixture
def mock_agent_one_skill():
    return agent_one_skill


agent_two_skills = copy.copy(agent_one_skill)
agent_two_skills["skills"].append(skill_with_model)


@pytest.fixture
def mock_agent_two_skills():
    return agent_two_skills


@pytest.fixture
def jpeg_attachment():
    file_path = "../tests/data/squeaky_bone.jpg"
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()
        encoded_image = base64.urlsafe_b64encode(image_data).decode("utf-8")
    return encoded_image


@pytest.fixture
def pdf_attachment():
    file_path = "../tests/data/dummy.pdf"
    with open(file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        encoded_pdf = base64.urlsafe_b64encode(pdf_data).decode("utf-8")
    return encoded_pdf


attachment_database = {
    "d0e478dd-dd1b-4e55-9beb-ec6c2c3f18d7": jpeg_attachment,
    "20a6737d-1fb6-4a63-9d9f-c0034d77153e": pdf_attachment,
}


@pytest.fixture
def mock_attachment_database():
    return attachment_database


chat_without_messages = {
    "ID": "81bddc2b-36e6-495a-a8e4-d5207a50f121",
    "name": "First Chat",
    "pinned": False,
    "bookmarked": True,
    "focused": False,
    "open": False,
    "to_delete": False,
    "last_accessed": dt.datetime(2023, 10, 4, 12, 0, 0),
    "agent": agent_one_skill,
}


@pytest.fixture
def mock_chat_without_messages():
    return chat_without_messages


chat_with_messages = chat_without_messages | {
    "messages": [
        lcm.HumanMessage(content="This is a basic human input message to the chat."),
        lcm.AIMessage(content="This is an AI response to the human message."),
        lcm.HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": "Please find me something like this image.",
                },
                {
                    "type": "image",
                    "source_type": "base64",
                    "mime_type": "image/jpeg",
                    "data": "d0e478dd-dd1b-4e55-9beb-ec6c2c3f18d7",
                },
            ]
        ),
    ]
}


@pytest.fixture
def mock_chat_with_messages():
    return chat_with_messages


additional_chat_without_messages = {
    "ID": "81bddc2b-36e6-495a-a8e4-d5207a50f121",
    "name": "Second Chat",
    "pinned": True,
    "bookmarked": False,
    "focused": True,
    "open": True,
    "to_delete": False,
    "last_accessed": dt.datetime(2024, 10, 4, 12, 0, 0),
    "agent": mock_agent_two_skills,
}


@pytest.fixture
def mock_additional_chat_without_messages():
    return additional_chat_without_messages


additional_chat_with_messages = additional_chat_without_messages | {
    " messages": [
        lcm.HumanMessage(content="This is a basic human input message to the chat."),
        lcm.AIMessage(content="This is an AI response to the human message."),
        lcm.HumanMessage(
            content=[
                {"type": "text", "text": "Summarize this document."},
                {
                    "type": "file",
                    "source_type": "base64",
                    "mime_type": "application/pdf",
                    "data": "20a6737d-1fb6-4a63-9d9f-c0034d77153e",
                },
            ]
        ),
    ]
}


@pytest.fixture
def mock_additional_chat_with_messages():
    return additional_chat_with_messages


chat_response = {
    "messages": [lcm.AIMessage(content="This is an AI response to the human message.")]
}


@pytest.fixture
def mock_chat_response():
    return chat_response


start_date = str(dt.date(1928, 11, 18))
end_date = str(dt.date(2026, 5, 1))
user = {
    "ID": "6b96666e-8b3a-4996-932d-3aa75c08c16f",
    "name": "Michael Luch",
    "start_date": "11-18-1928",
    "end_date": "5-1-2026",
    "available_credits": 26,
    "used_credits": 14,
    "location": "Anaheim, CA",
    "agents": [agent_one_skill, agent_two_skills],
    "chats": [chat_without_messages, additional_chat_without_messages],
}


@pytest.fixture
def mock_user():
    return user
