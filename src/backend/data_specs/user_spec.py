import typing as t
import pydantic as pyd
import datetime as dt

import backend.data_specs.agent_spec as agent
import backend.data_specs.chat_spec as chat
import backend.data_specs.base_types as base

UserID = t.NewType("UserID", str)

class UserTag(pyd.BaseModel):
    """
    Tag for identifying a unique user.
    """

    ID: UserID
    name: base.ShortName

class UserInfo(pyd.BaseModel):
    """
    Class which stores relevant information about the user.
    """
    subscriber: bool = False
    subscription_start: t.Optional[dt.datetime] = None
    subscription_end: t.Optional[dt.datetime] = None
    accrued_credits: t.Optional[int] = 0
    used_credit: t.Optional[int] = 0
    location: t.Optional[str] = None

class User(pyd.BaseModel):
    """
    Class which stores relevant information about the user.
    """
    tag: UserTag
    info: UserInfo
    agents: t.Optional[list[agent.AgentTag]] = None
    chats: t.Optional[list[chat.ChatTag]] = None


class UserMap(pyd.BaseModel):
    """
    Map of UserIDs to the associated User.
    This map should always be 1:1
    """

    __root__: pyd.Dict[UserID, User]

    def __init__(self, data: t.Iterable[User]):
        if isinstance(data, t.Iterable):
            super().__init__(
                __root__={customer.user.ID: customer for customer in data}
            )
        else:
            raise TypeError(
                f"ERROR instantiating a {self.__class__.__name__}:\n"
                f"Expected an iterable of User values, but got {type(data).__name__} instead."
            )