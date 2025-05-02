import uuid as u
import copy
import tests.api_fixtures as api_mocks
import fastapi as fapi

pike_router = fapi.APIRouter()


## Read calls
# c.iii.1 (?) get available agents
@pike_router.get("/agents")
def get_public_agents() -> list[dict]:
    """
    Get a list of all public agent types.
    """
    return [api_mocks.agent_one_skill, api_mocks.agent_two_skills]


# 1.d.  User settings
@pike_router.get("/user/{user_id}")
def get_user_info(user_id: str) -> dict:
    """
    Provides full info about a user given their user_id.
    """
    return api_mocks.user


# 1.a.  get my agents
@pike_router.get("/user/{user_id}/agents")
def get_user_agents(user_id: u.UUID) -> list[dict]:
    """
    Get all agents the user has chosen to enable.
    """
    return [api_mocks.agent_one_skill, api_mocks.agent_two_skills]


# 1.b.  get compact chat representations
@pike_router.get("/user/{user_id}/chats")
def get_user_chats_compact(user_id: str) -> list[dict]:
    """
    Gets a list of chat tags, providing enough information to render the associated
    chats without messages.
    """
    return (
        api_mocks.mock_chat_without_messages,
        api_mocks.mock_additional_chat_without_messages,
    )


# 2.a
@pike_router.get("/user/{user_id}/agent/{agent_id}/chats")
def get_user_chats_by_agent(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Return a list of all chats for a specific user which use a specific agent.
    """
    return api_mocks.mock_chat_without_messages


# 2.b (somwhat) get a chat's full history
@pike_router.get("/user/{user_id}/chat/{chat_id}")
def get_user_chat(user_id: str, chat_id: u.UUID) -> dict:
    """
    Provides the chat history for user {user_id} and thread {chat_id} in an
    appropriate format for sending to the frontend.
    """
    return api_mocks.mock_chat_with_messages


# 2.h Get attachment information.  (Should be implicitly filtered by user as attachments are in user's chats)
@pike_router.get("/attachment/{attachment_id}")
def get_attachment(attachment_id: u.UUID) -> str:
    """
    Uses an attachment_id to request the data from a specific attachment from the backend.
    """
    return api_mocks.mock_attachment_database.values()[0]


@pike_router.get("/agent/{agent_id}")
def get_agent(agent_id: u.UUID) -> dict:
    """
    Retrieve the information about a specific agent.
    """
    return api_mocks.mock_agent_two_skills


## Create calls
# 2.c Create a new chat
@pike_router.post("/user/{user_id}/agent/{agent_id}/chat")
def create_chat(user_id: str, agent_id: u.UUID) -> dict:
    """
    Generates a new, empty chat with a ChatID, attached to a specific user with a specific agent
    employed within the chat.
    """

    return api_mocks.mock_additional_chat_without_messages


# c.ii.  add agent (Ignore agent preparedness flag for now)
@pike_router.post("/user/{user_id}/agent/{agent_id}")
def add_agent_to_user(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Adds a new potential agent to the user's current agent list.
    """
    return api_mocks.mock_user["agents"].append(api_mocks.mock_agent_one_skill)


# 2.d (and 2.c.ii)
@pike_router.post("/user/{user_id}/chat/{chat_id}")
def invoke_chat(
    user_id: str, chat_id: u.UUID, input: str | list[dict]
) -> str | list[dict]:
    """
    Sends input to the agent and receives output dictionary with responses.
    """
    return api_mocks.mock_chat_response


##Deletion calls
# Delete agent from user
@pike_router.delete("/user/{user_id}/agent/{agent_id}")
def remove_agent_from_user(user_id: str, agent_id: u.UUID) -> list[dict]:
    """
    Removes the specified agent from the current user's list and returns the
    modified agent list for the user.
    """
    return [api_mocks.mock_agent_one_skill]


@pike_router.delete("/user/{user_id}/chat/{chat_id}")
def remove_chat_from_user(user_id: str, chat_id: u.UUID) -> list[dict]:
    """
    Deletes the specified chat history and removes the reference from the users
    list, returning the modified chat list for the user.
    """
    return [api_mocks.mock_user["chats"][:-1]]


##Put calls
# Change chat flags
@pike_router.put("/user/{user_id}/chat/{chat_id}")
def modify_chat_status(user_id: str, chat_id: u.UUID, chat_flags: dict) -> dict:
    """
    Modifies the chat flags included in the current chat to be those sent in the
    chat_flags object by the frontend.  Returns the modified chat without messages.
    """
    modified_chat = copy.copy(api_mocks.mock_chat_with_messages)
    modified_chat.pinned = True
    modified_chat.bookmarked = False
    modified_chat.open = True
    return modified_chat
