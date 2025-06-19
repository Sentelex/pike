import base64
import urllib
import os
import pathlib as pl
import importlib as il


TOOLS_PATH = il.resources.files("backend.src.tools")
#TOOLS_PATH = il.resources.files("src.tools")
ICONS_PATH = TOOLS_PATH / "icons"

def pad_base64(input_str: str) -> str:
    missing_padding = len(input_str) % 4
    if missing_padding:
        input_str += '=' * (4-missing_padding)
    return input_str

def encode_icon_url_safe_utf8(icon_name: str) -> str:
    """Encodes binary icon svg file to a URL-safe UTF-8 string."""
    icon_path = os.path.join(ICONS_PATH, icon_name)
    with open(icon_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        url_safe_string = urllib.parse.quote(encoded_string, safe="")
        return pad_base64(urllib.parse.unquote(url_safe_string))