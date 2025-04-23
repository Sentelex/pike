import uuid as u
import pydantic as pyd
import base64 as b64
import re

root_namespace = u.uuid.NAMESPACE_DNS
namespace_uuid = u.uuid5(root_namespace, "pike.sentelex.com")


class SafeUUID(pyd.ConstrainedStr):
    """
    A Pydantic-compatible URL-safe UUID string.
    """

    regex = re.compile(r"^[A-Za-z0-9_-]{22}$")

    def __new__(cls, value: str):
        if not cls.SAFE_UUID_REGEX.match(value):
            raise ValueError(f"Invalid SafeUUID: {value}")
        return super().__new__(cls, value)

    @classmethod
    def from_uuid(cls, raw_uuid: u.UUID) -> "SafeUUID":
        """
        Create a SafeUUID from a raw UUID.
        """
        safe_uuid_str = (
            b64.urlsafe_b64encode(raw_uuid.bytes).decode("utf-8").rstrip("=")
        )
        return cls.validate(safe_uuid_str)

    @classmethod
    def to_uuid(cls, safe_uuid: "SafeUUID") -> u.UUID:
        """
        Convert a SafeUUID back to a raw UUID.
        """
        # Add padding to make it a valid base64 string
        padded_safe_uuid = safe_uuid + "=" * (4 - len(safe_uuid) % 4)
        return u.UUID(bytes=b64.urlsafe_b64decode(padded_safe_uuid.encode("utf-8")))


def _str_to_uuid(input_string: str, uuid_base: u.UUID = namespace_uuid) -> u.UUID:
    """
    Generate a deterministic UUID based on the input string and the uuid_base
    Parameters
    ----------
    input_string : str
        The input string to generate the UUID from.
    uuid_base : u.UUID
        The base UUID to use as a hierarchical root.
    Returns
    -------
    u.UUID
        The generated UUID.
    """
    return u.uuid5(uuid_base, input_string)


def string_to_safe_uuid(specific: str, base_uuid: u.UUID = namespace_uuid) -> str:
    """
    Generate a URL-safe deterministic UUID based on the input string and the
    uuid_base

    Parameters
    ----------
    input_string : str
        The input string to generate the UUID from.
    uuid_base : u.UUID
        The base UUID to use as a hierarchical root.
    Returns
    -------
    u.UUID
        The generated UUID.
    """
    return SafeUUID.from_uuid(_str_to_uuid(specific, base_uuid))
