import typing as t
import collections.abc as ca
import langchain_core.messages as lcm
import uuid as u

import pydantic as pyd


class UserChatMap(pyd.BaseModel):
    """
    Map of users to the set of chats they have engaged in.
    """

    chat_tokens: set[chat.ChatTag]


ChatMap = dict[UserToken, tuple[UserName, set[ChatTag]]]

ChatRecap = tuple[UserName, ChatDescriptor, ca.Sequence[lcm.BaseMessage]]
