import typing as t
import pydantic as pyd
import datetime as dt
import langchain_core.messages as lcm

import agent_spec as agent
import base_types as base

ChatID = t.NewType("ChatID", base.ID)

class ChatFlags(pyd.BaseModel):
    """
    Flags for chat state.
    """
    is_pinned: bool = False
    is_bookmarked: bool = False
    is_open: bool = False
    is_focused: bool = False
    last_accessed: dt.datetime = dt.now()

class ChatTag(pyd.BaseModel):
    """
    Tag for identifying a unique chat.
    """
    ID: ChatID
    name: base.ShortName
    flags: ChatFlags
    agent: agent.AgentTag

class Chat(pyd.BaseModel):
    """
    Recap of a chat session.
    """
    tag: ChatTag
    messages: list[lcm.BaseMessage]

class ChatMap(pyd.BaseModel):
    """
    Map of ChatTokens to the associated Chat.
    This map should always be 1:1
    """

    __root__: pyd.Dict[ChatID, Chat]

    def __init__(self, data: t.Iterable[Chat]):
        if isinstance(data, t.Iterable):
            super().__init__(
                __root__={conversation.tag.ID : conversation for conversation in data}
            )
        else:
            raise TypeError(
                f"ERROR instantiating a {self.__class__.__name__}:\n"
                f"Expected an iterable of Chat values, but got {type(data).__name__} instead."
            )
