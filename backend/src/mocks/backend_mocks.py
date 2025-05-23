import uuid as u
import datetime as dt
from . import mock_api_interfaces as mapi
import backend.src.chat_type as ct

MOCK_USER_STORE = {
    "6b96666e-8b3a-4996-932d-3aa75c08c16f": {
        "name": "Michael Luch",
        "agents": [mapi.mock_agent_interface(), mapi.mock_agent_alt()],
        "chats" : ["81bddc2b-36e6-495a-a8e4-d5207a50f121",
                    "cabddc2b-36e6-495a-a8e4-d5207a50f122",
                    "c73782f0-30c2-472f-9d90-99c423eba897",
                    "80e89465-5117-477c-9b2e-e21b274bab48"]
    },
}

MOCK_CHAT_STORE = {
    "81bddc2b-36e6-495a-a8e4-d5207a50f121" : 
        ct.Chat(
            id="81bddc2b-36e6-495a-a8e4-d5207a50f121",
            agent="0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
            name="First Chat - Agent 1",
            created=dt.datetime(2023, 10, 4, 12, 0, 0),
            last_update=dt.datetime(2024, 10, 4, 12, 0, 0),
            opened=False,
            pinned=False,
            bookmarked=True,
            messages = mapi.mock_chat_history()["messages"],
        ),
    "cabddc2b-36e6-495a-a8e4-d5207a50f122" :
        ct.Chat(
            id="cabddc2b-36e6-495a-a8e4-d5207a50f122",
            agent="0e3c04dd-268a-45d8-8834-fd0e3e0c9f47",
            name="Second Chat - Agent 1",
            created=dt.datetime(2023, 10, 4, 15, 0, 0),
            last_update=dt.datetime(2023, 11, 4, 15, 0, 0),
            opened=True,
            pinned=False,
            bookmarked=False,
            messages = mapi.mock_chat_history_alt()["messages"],
        ),
    "c73782f0-30c2-472f-9d90-99c423eba897" :
        ct.Chat(
            id="c73782f0-30c2-472f-9d90-99c423eba897",
            agent="bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48",
            name="First Chat - Agent 2",
            created=dt.datetime(2023, 10, 4, 12, 0, 0),
            last_update=dt.datetime(2024, 10, 4, 12, 0, 0),
            opened=False,
            pinned=False,
            bookmarked=True,
            messages = mapi.mock_chat_history()["messages"],
        ),
    "80e89465-5117-477c-9b2e-e21b274bab48" :
        ct.Chat(
            id="80e89465-5117-477c-9b2e-e21b274bab48",
            agent="bf2e3e0c-268a-45d8-8834-fd0e3e0c9f48",
            name="Second Chat - Agent 2",
            created=dt.datetime(2023, 10, 4, 15, 0, 0),
            last_update=dt.datetime(2023, 11, 4, 15, 0, 0),
            opened=True,
            pinned=False,
            bookmarked=False,
            messages = mapi.mock_chat_history_alt()["messages"],
        )
    }


def get_user_chat_list(user_id: u.UUID) -> list[u.UUID]:
    """
    Returns a list of chat IDs for a given user.
    """

    if user_id in MOCK_USER_STORE:
        return MOCK_USER_STORE[user_id]["chats"]
    else:
        raise ValueError(f"User ID {user_id} not found.")

def get_user_chats(user_id: u.UUID) -> list[u.UUID]:
    """
    Returns a list of chats for a given user.
    """
    chat_ids = get_user_chat_list(user_id)
    chats = [MOCK_CHAT_STORE.get(id,None) for id in chat_ids]
    if None in chats:
        ids_found = [chat.id for chat in chats if chat is not None]
        ids_not_found = [id for id in chat_ids if id not in ids_found]
        unfound = '\n\t'.join(ids_not_found)
        raise ValueError(f"ERROR:  Could not find the following chat IDs belonging to user: {unfound}")
    return chats
