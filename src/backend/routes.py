import pike
import typing as t
import pydantic as pyd
import langchain_core.messages as lcm
import fastapi as fapi
import copy

import backend.data_specs.agent_spec as agent
import backend.data_specs.chat_spec as chat
import backend.data_specs.user_spec as user
import backend.data_specs.attachment_spec as attach

import test_data as teda

# See https://python.langchain.com/docs/how_to/multimodal_inputs/#documents-pdf for more info on the payload
class MultimodalContent(pyd.BaseModel):
    content: list[dict[str,str]]    

class InputMessage(pyd.BaseModel):
    """
    An input message that may have text input, a multimodal message input 
    dictionary, or both.
    """
    text: t.Optional[str] = None
    multimodal: t.Optional[MultimodalContent] = None

    @pyd.model_validator(mode="after")
    def validate_message(cls, model):
        """
        Ensure that at least one of 'text' or 'multimodal' is provided.
        """
        if not model.text and not model.multimodal:
            raise ValueError("InputMessage must contain either a text or multimodal payload.")
        return model


# User access calls


## Read calls
# c.iii.1 (?) get available agents
@pike.api.get("/agents")
async def get_public_agents() -> list[agent.Agent]:
    """
    Get a list of all public agent types.

    Returns
    -------
    agent_list: list[Agent]
    """
    return list(teda.all_agent_set)

# 1.d.  User settings
@pike.api.get("/user/{user_id}")
async def get_user_info(user_id: user.UserID) -> user.User:
    """
    Provides full info about a user given their user_id.

    Parameters:
    -----------
    user_id:  UserToken
      User's ID token from login

    Returns:
    --------
    user: User
      All information about a user
    """
    user_complete = teda.mickey_user
    return user_complete

# 1.a.  get my agents
@pike.api.get("/user/{user_id}/agents")
async def get_user_agents(user_id: user.UserID) -> list[agent.Agent]:
    """
    Get all agents the user has chosen to enable.

    Parameters
    ----------
    user_id:  UserToken
      User's ID token from login

    Returns
    -------
    agent_list: list[Agent]
      List of currently enabled agents for the user.
    """
    agent_list = teda.mickey_user.agents
    return agent_list

# 1.b.  get compact chat representations
@pike.api.get("/user/{user_id}/chats")
async def get_user_chats_compact(user_id: user.UserID) -> list[chat.ChatTag]:
    """
    Gets a list of chat tags, providing enough information to render the associated
    chats without messages.

    Parameters:
    -----------
    user_id:  UserToken
      User's ID token from login

    Returns:
    --------
    compact_chat_list: list[ChatTag]
      A list of compact representations (ChatTags) of chats in which the user has been
      involved
    """
    compact_chat_list = teda.mickey_user.chats
    return compact_chat_list

# 2.a
@pike.api.get("/user/{user_id}/agent/{agent_id}/chats")
async def get_user_chats_by_agent(user_id: user.UserID, agent_id: agent.AgentID)->list[chat.ChatTag]:
    """
    Return a list of all chats for a specific user which use a specific agent.

    Parameters
    ----------
    user_id: UserToken
      The token identifying the current user

    agent_id: UUID
      The UUID identifying the currently selected agent

    Returns
    -------
    chat_list: list[ChatTag]
      List of all chat tags belonging to this user which employ the specified agent.
    """
    # user_id = teda.mickey_user.tag.ID
    # user_chats = teda.mickey_user.chats
    # agent_id = teda.mickey_AgentTag_1
    # chat_list = [chat for chat in user_chats if chat.agent.ID == agent_id]
    chat_list = [teda.mickey_Chat1.tag]
    return chat_list

# 2.b (somwhat) get a chat's full history
@pike.api.get("/user/{user_id}/chat/{chat_id}")
async def get_user_chat(user_id: user.UserID, chat_id: chat.ChatID) -> chat.Chat:
    """
    Provides the chat history for user {user_id} and thread {chat_id} in an
    appropriate format for sending to the frontend.

    Parameters
    ----------
    user_id : UserToken
        The user token to identify the user.
    chat_id : ChatToken
        The thread ID associated with the user.

    Returns


    -------
    ChatRecap
        A ChatRecap object containing the user_id, the short name of the chat
        for the frontend, and the chat messages themselves.
    """
    return teda.mickey_Chat1
    # user_id = teda.mickey_token
    # chat_id = teda.chat_token_1
    # if not user_id in user_map:
    #     raise fapi.HTTPException(status_code=404, detail=f"User not found")
    # try:
    #     if not chat_id in user_map.values():
    #         raise fapi.HTTPException(
    #             status_code=404, detail=f"Requested chat not found"
    #         )
    #     return teda.chat_recap_example
    # except Exception as e:
    #     raise

# 2.h Get attachment information.  (Should be implicitly filtered by user as attachments are in user's chats)
@pike.api.get("/attachment/{attachment_id}")
async def get_attachment(attachment_id: attach.AttachmentID) -> attach.Attachment:
    """
    Uses an attachment_id to request the data from a specific attachment from the backend.

    Parameters
    ----------
    attachment_id:  The UUID of the attachment requested.
    """
    return teda.bbgun_Attach

@pike.api.get("/agent/{agent_id}")
async def get_agent(agent_id: agent.AgentID)-> agent.Agent:
    """
    Retrieve the information about a specific agent.

    Parameters
    ----------
    agent_id: UUID
      The ID of the agent about which to retrieve information.
    """

    return teda.default_Agent

## Create calls
# 2.c Create a new chat
@pike.api.post("/user/{user_id}/agent/{agent_id}/chat")
async def create_chat(user_id: user.UserID, agent_id: agent.AgentID)-> chat.ChatTag:
    """
    Generates a new, empty chat with a ChatID, attached to a specific user with a specific agent
    employed within the chat.


    Parameters
    ----------
    user_id: UserToken
      The token identifying the current user

    agent_id: UUID
      The UUID identifying the currently selected agent

    Returns
    -------
    chat_tag: ChatTag
      A ChatTag representing the newly created chat.
    """
    # Faux user lookup to get username
    user = teda.mickey_user
    # Faux lokup for agent info
    agent = teda.default_Agent
    new_chatTag = chat.ChatTag(
        ID=teda.new_chatID,
        name=f"NewChat - {user.tag.name} - {agent.tag.name}",
        flags=chat.ChatFlags(
            is_open=True,
            is_focused=True
        ),
        agent = agent.tag
    )
    return new_chatTag

# c.ii.  add agent (Ignore agent preparedness flag for now)
@pike.api.post("/user/{user_id}/agent/{agent_id}")
async def add_agent_to_user(
    user_id: user.UserID, agent_id: agent.AgentID
) -> list[agent.Agent]:
    """
    Adds a new potential agent to the user's current agent list.

    Parameters
    ----------
    user_id: UserToken
      User's ID token from login
    agent_id: UUID
      ID of the agent to add to the user's list

    Returns:
    --------
    new_agent_list:  list[Agent]
      New list of agents for user
    """
    teda.mickey_user.agents.append(teda.additional_Agent)
    return teda.mickey_user.agents

# 2.d (and 2.c.ii)
@pike.api.post("/user/{user_id}/chat/{chat_id}")
async def invoke_chat(user_id: user.UserID, chat_id: chat.ChatID, input: InputMessage) -> lcm.BaseMessage:

  config = {"configurable": {"thread_id": chat_id}}

  try:
    if input.text:
      message_body = {"role" : "user", "content" : input.text}
    else:
      message_body = {"role" : "user", "content" : input.multimodal.model_dump()}
    
    responses = []
    for event in pike.graph.stream( {"messages" : [message_body]}, 
                              config ):
        for value in event.values():
            responses.append(value["messages"].content)
    return {"responses" : responses[0] if responses else "..."}
  
  except Exception as err:
    print(f"Error in invoke_chat: {str(err)}")
    raise fapi.HTTPException(status_code=500, detail=str(err))

##Deletion calls
# Delete agent from user
@pike.api.delete("/user/{user_id}/agent/{agent_id}")
async def remove_agent_from_user(user_id: user.UserID, agent_id: agent.AgentID) -> list[agent.Agent]:
    """
    Removes a curent agent from the user's current agent list.

    Parameters
    ----------
    user_id: UserToken
      User's ID token from login
    agent_id: UUID
      ID of the agent to remove from the user's list

    Returns:
    --------
    new_agent_list:  list[Agent]
      Adjusted list of agents for the user
    """
    if teda.additional_Agent in teda.mickey_user.agents:
        teda.mickey_user.agents.pop(teda.additional_Agent)
    return teda.mickey_user.agents

@pike.api.delete("/user/{user_id}/chat/{chat_id}")
async def remove_chat_from_user(user_id: user.UserID, chat_id: chat.ChatID)->list[chat.ChatTag]:
    """
    Deletes a chat and all associated information, unlinking it from a user's history.

    Parameters
    ----------
    user_id : UserToken
      The chat owner's ID
    chat_id : UUID
      The chat identifier of the chat to be deleted.

    Returns
    -------
      The updated list of chat tags belonging to the user after deletion.
    """

    return copy.copy(teda.mickey_user_chats).pop(teda.mickey_ChatTag_2)

##Put calls
# Change chat flags
@pike.api.put("/user/{user_id}/chat/{chat_id}")
async def modify_chat_status(user_id: user.UserID, chat_id: chat.ChatID, chat_flags: chat.ChatFlags)->chat.ChatTag:
    """
    Modifies the flags controlling a chat's state (pinned, bookmarked, open, etc...)

    Parameters
    ----------
    user_id : UserToken
      ID of the user owning the chat
    chat_id : UUID
      Identifier for the chat being modified
    chat_flags : ChatFlags
      The flags and their respective desired states

    Returns
    -------
      The updated ChatTag for the chat whose flags were modified.
    """
    
    return (chat.ChatTag(teda.mickey_Chat1.tag.ID,
                         teda.mickey_Chat1.tag.name,
                         chat_flags,
                         teda.mickey_Chat1.tag.agent))