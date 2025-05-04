import uuid as u
import copy
import tests.api_fixtures as api_mocks
import fastapi as fapi

pike_router = fapi.APIRouter()


@pike_router.get("/agents")
def get_public_agents() -> list[dict]:
    """
    Get a list of all public agent types.
    """
    return [api_mocks.mock_agent_interface]


@pike_router.get("/user/{user_id}")
def get_user_info(user_id: str) -> dict:
    """
    Provides full info about a user given their user_id.
    """
    return api_mocks.user_user_info


@pike_router.get("/user/{user_id}/agents")
def get_user_agents(user_id: u.UUID) -> list[dict]:
    """
    Get all agents the user has chosen to enable.
    """
    return [api_mocks.mock_agent_interface, api_mocks.mock_agent_alt]


@pike_router.get("/user/{user_id}/chats")
def get_user_chats(user_id: str, agent_id) -> list[dict]:
    """
    Gets a list of chat tags, providing enough information
    to render the associated chats without messages.
    """
    return [
        api_mocks.mock_chat_interface,
        api_mocks.mock_chat_alt,
    ]


@pike_router.get("/user/{user_id}/chat/{chat_id}")
def get_chat_history(chat_id: u.UUID) -> dict:
    """
    Provides the chat history for user {user_id} and thread {chat_id} in an
    appropriate format for sending to the frontend.
    """
    return api_mocks.mock_chat_history


@pike_router.get("/attachment/{attachment_id}")
def get_attachment(attachment_id: u.UUID) -> str:
    """
    Uses an attachment_id to request the data from a specific attachment from the backend.
    """
    return api_mocks.mock_pdf_attachment


@pike_router.get("/agent/{agent_id}")
def get_agent(agent_id: u.UUID) -> dict:
    """
    Retrieve the information about a specific agent.
    """
    return api_mocks.mock_agent_alt


@pike_router.post("/user/{user_id}/agent/{agent_id}/chat")
def create_chat(user_id: str, agent_id: u.UUID) -> dict:
    """
    Generates a new, empty chat with a ChatID, attached to a specific user with a specific agent
    employed within the chat.
    """

    return api_mocks.mock_chat_alt


@pike_router.post("/user/{user_id}/agent/{agent_id}")
def add_agent_to_user(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Adds a new potential agent to the user's current agent list.
    """
    return [api_mocks.mock_agent, api_mocks.mock_agent_alt]


@pike_router.post("/user/{user_id}/chat/{chat_id}")
def get_response(
    chat_id: u.UUID, input: str | list[dict], attachment: str = None
) -> str | list[dict]:
    """
    Sends input to the agent and receives output dictionary with responses.
    """
    return api_mocks.mock_chat_response


@pike_router.delete("/user/{user_id}/agent/{agent_id}")
def remove_agent_from_user(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Removes the specified agent from the current user's list and returns the
    modified agent list for the user.
    """
    return [api_mocks.mock_agent_interface]


@pike_router.delete("/user/{user_id}/chat/{chat_id}")
def remove_chat_from_user(user_id: str, chat_id: u.UUID) -> list[dict]:
    """
    Deletes the specified chat history and removes the reference from the users
    list, returning the modified chat list for the user.
    """
    return [api_mocks.mock_chat_interface]


@pike_router.put("/user/{user_id}/chat/{chat_id}")
def modify_chat_status(chat_id: u.UUID, chat_flags: dict) -> dict:
    """
    Modifies the chat flags included in the current chat to be those sent in the
    chat_flags object by the frontend.  Returns the modified chat without messages.
    """
    modified_chat = copy.copy(api_mocks.mock_chat_history)
    modified_chat.pinned = True
    modified_chat.bookmarked = False
    modified_chat.open = True
    return modified_chat
