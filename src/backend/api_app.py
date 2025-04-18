import contextlib as cl
import fastapi as fapi
import fastapi.middleware.cors as fapi_cors

from .typedefs import *
from test_data import test_chat_map, chat_recap_example

import langchain_core.messages as lcm


def get_user_chat_map() -> ChatMap:
    """
    Get the user thread map storing the threads associated with each user.
    Returns
    -------
    dict
        Dictionary mapping UserToken to list of ThreadIdentifiers.
    """
    # This is a placeholder function. In a real application, this would fetch
    # data from a database or other storage.
    return test_chat_map


user_map = {}


@cl.asynccontextmanager
async def service_lifecycle(app: fapi.FastAPI):
    """
    Lifecycle context manager for FastAPI app.

    Parameters
    ----------
    app : fapi.FastAPI
        FastAPI app instance.

    Yields
    ------
    None
    """
    # Should we actually have a server singleton here to hold things like the
    #   user_map and other server state variables (database, )
    user_map = get_user_chat_map()
    # Startup: Initialize things that need to be in place before the backend starts
    # e.g. database connections, prefect initialization, etc.

    # Run the app:
    yield

    # Shutdown: Perform any cleanup tasks that need to be done before server shutdown
    # e.g. close database connections, stop background tasks, etc.

    # save_user_map(user_map) # For eventual use when we have a database
    del user_map


pike_api = fapi.FastAPI(lifespane=service_lifecycle)

pike_api.add_middleware(
    fapi_cors.CORSMiddleware,
    allow_origins=["http://localhost", "https://localhost", "https://localhost:8080"],
    # Should be restricted to designated front ends for production/testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@pike_api.get("/agent_list")
async def get_agent_types() -> list[str]:
    """
    Get a list of all agent types.

    Returns
    -------
    list of str
        List of agent types.
    """
    return ["agent1", "agent2", "agent3"]


@pike_api.get("/user/{user_id}/chat")
async def get_chats(user_id: UserToken) -> list[ChatToken]:
    """
    Provides a list of all thread ids which are associated with the specific user.

    Parameters
    ----------
    user : UserToken
        The user token to identify the user.

    Returns
    -------
    list of ThreadToken
        List of thread IDs associated with the user.
    """
    if len(user_map.keys()) != 0:
        try:
            chat_list = user_map[user_id]
            return user_map[user_id]
        except KeyError as ke:
            ke.message = f"User not found in user database."
            raise fapi.HTTPException(
                status_code=404, detail=f"User {user_id} not found"
            ) from ke
    else:  # We don't have a user_map with any users mapped.
        pass


@pike_api.get("/user/{user_id}/chat/{chat_id}")
async def get_history(user_id: UserToken, chat_id: ChatToken) -> ChatRecap:
    """
    Provides the chat history for user {user_id} and thread {chat_id} in an
    appropriate format for sending to the frontend.

    Parameters
    ----------
    user : UserToken
        The user token to identify the user.
    chat_id : ChatToken
        The thread ID associated with the user.

    Returns
    -------
    ChatRecap
        A ChatRecap object containing the user_id, the short name of the chat
        for the frontend, and the chat messages themselves.
    """
    if not UserToken in user_map:
        raise fapi.HTTPException(status_code=404, detail=f"User not found")
    try:
        if not chat_id in user_map.values():
            raise fapi.HTTPException(
                status_code=404, detail=f"Requested chat not found"
            )
        return chat_recap_example
    except Exception as e:
        raise
