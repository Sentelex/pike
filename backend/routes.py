import uuid as u
import copy
import fastapi as fapi
import pydantic as pyd
import langchain_core.messages as lcm

import src.mocks.mock_api_interfaces as mapi
import src.mocks.backend_mocks as bm
import src.chat as ct
import src.graph_builder as gb

pike_router = fapi.APIRouter()


class ChatInput(pyd.BaseModel):
    message: str
    attachment: dict | None = None


def chat_to_interface(chat: ct.Chat) -> dict:
    """
    Converts a Chat object to a dictionary suitable for API response.
    """
    return {
        "chatId": str(chat.id),
        "chatName": chat.name,
        "isOpen": chat.opened,
        "isPinned": chat.pinned,
        "isBookmarked": chat.bookmarked,
        "createdAt": chat.created.isoformat(),
        "updatedAt": chat.last_update.isoformat(),
        "agentId": str(chat.agent_id)
    }


CHAT_STORE_PROXY = copy.deepcopy(bm.MOCK_CHAT_STORE)


@pike_router.get("/agents")
def get_public_agents() -> list[dict]:
    """
    Get a list of all public agent types.
    """
    return [mapi.mock_agent_interface()]


@pike_router.get("/user/{userId}")
def get_user_info(userId: str) -> dict:
    """
    Provides full info about a user given their userId.
    """
    return mapi.mock_user_info()


@pike_router.get("/user/{userId}/agents")
def get_user_agents(userId: str) -> list[dict]:
    """
    Get all agents the user has chosen to enable.
    """
    return [mapi.mock_agent_interface(), mapi.mock_agent_alt()]


@pike_router.get("/user/{userId}/agent/{agentId}/chats")
def get_user_chats(userId: str, agentId: u.UUID) -> list[dict]:

    # TODO update this to use CHAT_CACHE from chat.py
    """
    Gets a list of chats for the specific user and agent.
    """
    if agentId == u.UUID("0e3c04dd-268a-45d8-8834-fd0e3e0c9f47"):
        # Return chats for agent one
        print("0e3c04dd-268a-45d8-8834-fd0e3e0c9f47")
        return [
            mapi.mock_chat_interface(),
            mapi.mock_chat_alt(),
        ]
    elif agentId == u.UUID("bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48"):

        # Return a different set of chats for agent two
        print("bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48")
        return [
            mapi.mock_chat_interface_2(),
            mapi.mock_chat_alt_2(),
        ]
    else:
        # For any other agent_id, you could return an empty list or a default
        print("no agentId matched")
        return []


@pike_router.get("/user/{userId}/pinned-chats")
def get_user_pinned_chats(userId: str) -> list[dict]:
    """
    Gets a list of pinned chats for a particular user.
    """
    return mapi.mock_pinned_chats_list()


@pike_router.get("/chat/{chatId}/history")
def get_chat_history(chatId: u.UUID) -> dict:
    """
    Provides the chat history for user {userId} and thread {chatId} in an
    appropriate format for sending to the frontend.
    """
    if chatId not in ct.CHAT_CACHE:
        raise fapi.HTTPException(
            status_code=404,
            detail=f"Chat with ID {chatId} not found."
        )
    return {"messages": ct.CHAT_CACHE[chatId].messages}


@pike_router.get("/attachment/{attachmentId}")
def get_attachment(attachmentId: u.UUID) -> str:
    """
    Uses an attachmentId to request the data from a specific attachment from the 
    """
    return mapi.mock_pdf_attachment()


@pike_router.get("/agent/{agentId}")
def get_agent(agentId: u.UUID) -> dict:
    """
    Retrieve the information about a specific agent.
    """
    return mapi.mock_agent_alt()


@pike_router.post("/user/{userId}/agent/{agentId}/create_chat/{chatId}")
def create_chat(userId: str, agentId: u.UUID, chatId: u.UUID, body: ChatInput) -> dict:
    """
    Generates a new chat with a chatId, attached to a specific user with a specific agent
    employed within the chat and a first message.
    """
    ct.CHAT_CACHE[chatId] = ct.Chat(
        id=chatId,
        agent_id=agentId,
        new_message=lcm.HumanMessage(body.message),
        attachment=body.attachment
    )
    message = gb.get_response(chatId, body.attachment)
    return {'newChat': chat_to_interface(ct.CHAT_CACHE[chatId]),
            'message': message}


@pike_router.post("/user/{userId}/agent/{agentId}/add")
def add_agent_to_user(userId: str, agentId: u.UUID) -> list[dict]:
    """
    Adds a new potential agent to the user's current agent list.
    """
    return [mapi.mock_agent_interface(), mapi.mock_agent_alt()]


@pike_router.post("/chat/{chatId}/response")
def get_response(chatId: u.UUID, body: ChatInput) -> dict:
    """
    Sends input to the agent and receives output dictionary with responses.
    """
    return gb.get_response(chatId, body.attachment)


@pike_router.delete("/user/{userId}/agent/{agentId}/delete")
def remove_agent_from_user(userId: str, agentId: u.UUID) -> list[dict]:
    """
    Removes the specified agent from the current user's list and returns the
    modified agent list for the user.
    """
    return [mapi.mock_agent_interface()]


@pike_router.delete("/user/{userId}/chat/{chatId}/delete")
def remove_chat_from_user(userId: str, chatId: u.UUID) -> list[dict]:
    """
    Deletes the specified chat history and removes the reference from the users
    list, returning the modified chat list for the user.
    """
    return [mapi.mock_chat_interface()]


@pike_router.put("/chat/{chatId}/status")
def modify_chat_status(chatId: u.UUID, chat_flags: dict) -> dict:
    """
    Modifies the chat flags included in the current chat to be those sent in the
    chat_flags object by the frontend.  Returns the modified chat without messages.
    """
    if chatId not in ct.CHAT_CACHE:
        raise fapi.HTTPException(
            status_code=404,
            detail=f"Chat with ID {chatId} not found."
        )
    for key, value in chat_flags.items():
        setattr(ct.CHAT_CACHE[chatId], key, value)
    return chat_to_interface(ct.CHAT_CACHE[chatId])
