import uuid as u
import copy
import src.mocks.mock_api_interfaces as mapi
import src.mocks.backend_mocks as bm
import fastapi as fapi
import pydantic as pyd
import datetime as dt
import src.chat_type as ct
import langchain_core.messages as lcm

pike_router = fapi.APIRouter()


class ChatInput(pyd.BaseModel):
    message: str
    attachment: dict | None = None

# Generic interface translations extracted from work building the chat class.
    # def interface_be2fe(self) -> dict:
    #     """
    #     Dumps the chat interface for the frontend.
    #     """
    #     data = {
    #             "chatId": str(chat.id),
    #             "chatName": chat.name,
    #             "isOpen": chat.opened,
    #             "isPinned": chat.pinned,
    #             "isBookmarked": chat.bookmarked,
    #             "createdAt": chat.created.isoformat(),
    #             "updatedAt": chat.last_update.isoformat(),
    #             "agentId": str(chat.agent)
    #         }
    #     return json.dumps(data, indent=4)
    
    # def history_be2fe(self) -> dict:
    #     """
    #     Dumps the chat history for the frontend.
    #     """
    #     fields = ["content", "additional_kwargs", "type"]
    #     data = { "messages": 
    #         [ {field : getattr(msg, field, None) for field in fields}   
    #             for msg in chat.messages]
    #         }        
    #     return json.dumps(data, indent=4)

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
    """
    Gets a list of chats for the specific user and agent.
    """

    # Use "6b96666e-8b3a-4996-932d-3aa75c08c16f" for userId to return mocked 
    # data.
    user_chats = bm.get_user_chats(userId)
    return [chat for chat in user_chats if chat.agent == agentId]


@pike_router.get("/user/{userId}/pinned-chats")
def get_user_pinned_chats(userId: str) -> list[dict]:
    """
    Gets a list of pinned chats for a particular user.
    """
    user_chats = mapi.get_user_chatlist(userId)
    return [chat for chat in user_chats if chat.pinned]


@pike_router.get("/chat/{chatId}/history")
def get_chat_history(chatId: u.UUID) -> dict:
    """
    Provides the chat history for user {userId} and thread {chatId} in an
    appropriate format for sending to the frontend.
    """
    if chatId in bm.MOCK_CHAT_STORE:
        return bm.MOCK_CHAT_STORE[chatId].messages
    return None

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
    chat_id_search = [chat.id for chat in mapi.get_user_chat_list()]
    if chatId in chat_id_search: # Error, duplicate chatid.
        return {'error': 'Chat ID already exists.'}
    
    # BEGIN MOCK
    # Mock for generating the chat name, perhaps via LLM summary of the 
    # first message.
    chat_name = f"New chat : {body['message'][:10]}"
    # END MOCK

    new_chat = ct.Chat(
        id=chatId,
        agent=agentId,
        name=chat_name,
        created=dt.datetime.now(),
        last_update=dt.datetime.now(),
        messages = []
    )

    response = get_response(chatId, body)

    # BEGIN MOCK
    # Mock for adding the new chat to the chat store
    CHAT_STORE_PROXY[new_chat.id] = new_chat
    # END MOCK

    return {'newChat':{
                        'chatId': str(new_chat.id),
                        'chatName': new_chat.name,
                        'isOpen': new_chat.opened,
                        'isPinned': new_chat.pinned,
                        'isBookmarked': new_chat.bookmarked,
                        'createdAt': new_chat.created.isoformat(),
                        'updatedAt': new_chat.last_update.isoformat(),
                        'agentId': str(new_chat.agent)
                    },
            'message': response
        }


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
    ## BEGIN MOCK
    # Mock for loading chat history, getting agent graph, etc..
    if chatId not in CHAT_STORE_PROXY:
        return {'error': 'Chat ID not found.'}
    chat = CHAT_STORE_PROXY[chatId]
    ## END MOCK

    message_contents = []
    if body.message is not None:
        message_contents.append(
            {"type": "text", "text": body.message}
        )
    if body.attachment is not None:
        #  Attachment is directed to a url available to the LLM model
        if body.attachment.source == "url":
            message_contents.append(
                {"type": body.attachment.type,
                 "source_type": "url",
                 "url": body.attachment.url
                })
        #  Attachment is data provided directly via the message
        elif body.attachment.source == "base64":
            message_contents.append(
                {"type": body.attachment.type,
                 "source_type": "base64",
                 "mime_type": body.attachment.mime_type,
                 "data": body.attachment.data,
                })
        #  Source type is unrecognized.
        message = lcm.HumanMessage(contents=message_contents)

        # --BEGIN MOCK
        #  Normal invocation with the lggm.add_messages annotation will 
        #    automatically add these messages to history, but here for mocking 
        #    we do it by hand.
        chat.messages.append(message)          
        chat.messages.append(lcm.AIMessage(contents="This is an AI response to the human message."))
        # --END MOCK

    return dict(chat.messages[-1])


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
    modified_chat = copy.copy(mapi.mock_chat_interface())
    modified_chat["pinned"] = True
    modified_chat["bookmarked"] = False
    modified_chat["open"] = True
    return modified_chat
