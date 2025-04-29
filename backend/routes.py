import base64

import backend.pike as pike
import langchain_core.messages as lcm
import datetime as dt

import uuid as u


model_additional = {
    "temperature": 0.5,
    "max_tokens": 250,
}

model = {
    "model_name": "gpt-4o-mini",
    "api_key": "N0T-4-R34L-K3Y",
    "additonal_arguments": model_additional,
}

skill_1 = {
    "ID": "8365d252-1bf2-46da-b621-5450e31eb90d",
    "name": "PDF Reader",
    "description": "Parses main-body text from PDFs",
}

skill_2 = {
    "ID": "728f0e28-1d15-4934-92c4-a236f01acb9a",
    "name": "Summarizer",
    "description": "Summerizes provided text into a three sentence description.",
    "model": model,
}

agent_1 = {
    "ID": "0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
    "name": "Default Agent",
    "description": "PIKE's default agent",
    "model": model,
    "skills": [skill_1],
}

agent_2 = {
    "ID": "5461e31d-cbe0-4278-8c7e-a0a4ecd9d7b7",
    "name": "Additional Agent",
    "description": "Agent which does cool stuff",
    "model": model,
    "skills": [skill_1, skill_2],
}

file_path = "../tests/data/squeaky_bone.jpg"
with open(file_path, "rb") as image_file:
    image_data = image_file.read()
    encoded_image = base64.urlsafe_b64encode(image_data).decode("utf-8")

file_path = "../tests/data/dummy.pdf"
with open(file_path, "rb") as pdf_file:
    pdf_data = pdf_file.read()
    encoded_pdf = base64.urlsafe_b64encode(pdf_data).decode("utf-8")

attachment_db = {
    "d0e478dd-dd1b-4e55-9beb-ec6c2c3f18d7": encoded_image,
    "20a6737d-1fb6-4a63-9d9f-c0034d77153e": encoded_pdf,
}

chat_1_no_message = {
    "ID": "81bddc2b-36e6-495a-a8e4-d5207a50f121",
    "name": "First Chat",
    "pinned": True,
    "bookmarked": False,
    "focused": True,
    "open": True,
    "to_delete": False,
    "last_accessed": dt.datetime(2023, 10, 4, 12, 0, 0),
    "agent": agent_1,
}
chat_1 = {chat_1_no_message} | {
    "messages": [
        lcm.HumanMessage(content="This is a basic human input message to the chat."),
        lcm.AIMessage(content="This is an AI response to the human message."),
        lcm.HumanMessage(
            content=[
                {"type": "text", "text": "Please find me something like this image."},
                {
                    "type": "image",
                    "source_type": "base64",
                    "mime_type": "image/jpeg",
                    "data": attachment_db["d0e478dd-dd1b-4e55-9beb-ec6c2c3f18d7"],
                },
            ]
        ),
    ]
}

chat_2_no_message = {
    "ID": "81bddc2b-36e6-495a-a8e4-d5207a50f121",
    "name": "Second Chat",
    "pinned": True,
    "bookmarked": False,
    "focused": True,
    "open": True,
    "to_delete": False,
    "last_accessed": dt.datetime(2024, 10, 4, 12, 0, 0),
    "agent": agent_2,
}
chat_2 = {chat_2_no_message} | {
    "messages": [
        lcm.HumanMessage(content="This is a basic human input message to the chat."),
        lcm.AIMessage(content="This is an AI response to the human message."),
        lcm.HumanMessage(
            content=[
                {"type": "text", "text": "Summarize this document."},
                {
                    "type": "file",
                    "source_type": "base64",
                    "mime_type": "application/pdf",
                    "data": attachment_db["20a6737d-1fb6-4a63-9d9f-c0034d77153e"],
                },
            ]
        ),
    ]
}


chat_message = {
    "messages": [lcm.AIMessage(content="This is an AI response to the human message.")]
}

user = {
    "ID": "6b96666e-8b3a-4996-932d-3aa75c08c16f",
    "name": "Michael Luch",
    "start_date": dt.date(1928, 11, 18),
    "end_date": dt.date(2026, 5, 1),
    "available_credits": 26,
    "used_credits": 14,
    "location": "Anaheim, CA",
    "agents": [agent_1, agent_2],
    "chats": [chat_1, chat_2],
}


## Read calls
# c.iii.1 (?) get available agents
@pike.api.get("/agents")
def get_public_agents() -> list[dict]:
    """
    Get a list of all public agent types.
    """
    return [agent_1, agent_2]


# 1.d.  User settings
@pike.api.get("/user/{user_id}")
def get_user_info(user_id: str) -> dict:
    """
    Provides full info about a user given their user_id.
    """
    return user


# 1.a.  get my agents
@pike.api.get("/user/{user_id}/agents")
def get_user_agents(user_id: u.UUID) -> list[dict]:
    """
    Get all agents the user has chosen to enable.
    """
    [agent_1, agent_2]


# 1.b.  get compact chat representations
@pike.api.get("/user/{user_id}/chats")
def get_user_chats_compact(user_id: str) -> list[dict]:
    """
    Gets a list of chat tags, providing enough information to render the associated
    chats without messages.
    """
    return [chat_1_no_message, chat_2_no_message]


# 2.a
@pike.api.get("/user/{user_id}/agent/{agent_id}/chats")
def get_user_chats_by_agent(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Return a list of all chats for a specific user which use a specific agent.
    """
    return [chat_1_no_message]


# 2.b (somwhat) get a chat's full history
@pike.api.get("/user/{user_id}/chat/{chat_id}")
def get_user_chat(user_id: str, chat_id: u.UUID) -> dict:
    """
    Provides the chat history for user {user_id} and thread {chat_id} in an
    appropriate format for sending to the frontend.
    """
    return chat_1


# 2.h Get attachment information.  (Should be implicitly filtered by user as attachments are in user's chats)
@pike.api.get("/attachment/{attachment_id}")
def get_attachment(attachment_id: u.UUID) -> str:
    """
    Uses an attachment_id to request the data from a specific attachment from the backend.

    Parameters
    ----------
    attachment_id:  The UUID of the attachment requested.
    """
    return encoded_image


@pike.api.get("/agent/{agent_id}")
def get_agent(agent_id: u.UUID) -> dict:
    """
    Retrieve the information about a specific agent.
    """
    return agent_1


## Create calls
# 2.c Create a new chat
@pike.api.post("/user/{user_id}/agent/{agent_id}/chat")
def create_chat(user_id: str, agent_id: u.UUID) -> dict:
    """
    Generates a new, empty chat with a ChatID, attached to a specific user with a specific agent
    employed within the chat.
    """

    return chat_1_no_message


# c.ii.  add agent (Ignore agent preparedness flag for now)
@pike.api.post("/user/{user_id}/agent/{agent_id}")
def add_agent_to_user(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Adds a new potential agent to the user's current agent list.
    """
    return [agent_1, agent_2]


# 2.d (and 2.c.ii)
@pike.api.post("/user/{user_id}/chat/{chat_id}")
def invoke_chat(
    user_id: str, chat_id: u.UUID, input: str | list[dict]
) -> str | list[dict]:
    """
    Sends input to the agent and receives output dictionary with responses.
    """
    return chat_message


##Deletion calls
# Delete agent from user
@pike.api.delete("/user/{user_id}/agent/{agent_id}")
def remove_agent_from_user(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Removes the specified agent from the current user's list and returns the
    modified agent list for the user.
    """
    return [agent_1]


@pike.api.delete("/user/{user_id}/chat/{chat_id}")
def remove_chat_from_user(user_id: str, chat_id: u.UUID) -> list[dict]:
    """
    Deletes the specified chat history and removes the reference from the users
    list, returning the modified chat list for the user.
    """
    return [chat_1]


##Put calls
# Change chat flags
@pike.api.put("/user/{user_id}/chat/{chat_id}")
def modify_chat_status(user_id: str, chat_id: u.UUID, chat_flags: dict) -> dict:
    """
    Modifies the chat flags included in the current chat to be those sent in the
    chat_flags object by the frontend.  Returns the modified chat without messages.
    """
    return chat_1_no_message
