import pydantic as pyd
import data_specs.user_spec as user
import data_specs.chat_spec as chat


class UserChat(pyd.BaseModel):
    """
    Map of users to the set of chats they have engaged in.
    """

    __root__: pyd.Dict[user.UserID, pyd.Set[chat.ChatTag]]

    def __init__(self, data: pyd.Dict[user.UserID, pyd.Set[chat.ChatTag]]):
        super().__init__(__root__=data)