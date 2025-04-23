import hashlib as h
import base64
import uuid as u
import typedefs as td
import user_spec as user
import chat_spec as chat
import agent_spec as agent
import uuid_hierarchy as uh




test_chat_map = {
    UserToken(h.sha512(("MickeyMouse" + "MinnieR0XX").encode("UTF-8")).hexdigest()): {
        (
            "Mickey Mouse",
            set(
                [                  
                chat.ChatTag(
                        chat.ChatDescriptor("Pluto Gift Ideas"), 
                        uh.string_to_safe_uuid("Pluto")
                ),
                chat.ChatTag(
                        chat.ChatDescriptor("Minnie Gift Ideas"),
                        uh.string_to_safe_uuid("Minnie"),
                )
                ]
                ),                    
        )
    }
}

def encode_url_safe(base_uuid: u.UUID)->td.

def string_to_safe_uuid(base_uuid: u.UUID, specific: str) -> str:
    """
    Generate a URL-safe UUID based on a specific string.
    Parameters
    ----------
    base_uuid : u.UUID
        The base UUID to use as a namespace.
    specific : str
        The specific string to generate the UUID from.
    Returns
    -------
    str
        The URL-safe UUID as a string.
    """
    raw_uuid = u.uuid5(base_uuid, specific)
    safe_uuid = base64.urlsafe_b64encode(raw_uuid.bytes).decode("utf-8").rstrip("=")
    return safe_uuid


bbgun_uuid = string_to_safe_uuid(namespace_uuid, "RedRyder.jpg")
bone_uuid = string_to_safe_uuid(namespace_uuid, "SqueakyBone.jpg")

# Eventually the txt value here would actually be a UUEncoded binary string of
# the actual .jpg.
fake_attachment_db = {
    bbgun_uuid: "bbgun.jpg",
}

chat_recap_example = (
    UserName("Mickey Mouse"),
    ChatDescriptor("Pluto Gift Ideas"),
    [
        lcm.SystemMessage(
            content="You are a helpful assistant good at picking out gifts for a very good boy.\n ",
        ),
        lcm.HumanMessage(
            content="Please help me pick out a gift for my dog, Pluto.\n ",
        ),
        lcm.AIMessage(
            content="He might like an official Red Ryder carbine-action 200-shot range model air rifle\n ",
            additional_kwargs={"RedRyder.jpg": bbgun_uuid},
        ),
        lcm.HumanMessage(
            content="I don't think so, he's a pacifist.  How about a squeaky bone?\n ",
            additional_kwargs={"SqueakyBone.jpg": bone_uuid},
        ),
        lcm.AIMessage(
            content="Okay then, here is a link to a well-reviewed squeaky toy site: \nhttp://www.squeakytoy.ai ",
        ),
    ],
)
