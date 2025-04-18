import typing as t
import collections.abc as ca
import langchain_core.messages as lcm
import uuid as u

ChatToken = t.NewType("ChatToken", u.UUID)
ChatDescriptor = t.NewType("ChatDescriptor", str)
ChatTag = tuple[ChatDescriptor, ChatToken]

UserToken = t.NewType("UserToken", str)
UserName = t.NewType("UserName", str)
User = dict[UserToken, UserName]

ChatMap = dict[UserToken, tuple[UserName, set[ChatTag]]]

ChatRecap = tuple[UserName, ChatDescriptor, ca.Sequence[lcm.BaseMessage]]
