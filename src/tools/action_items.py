from langchain_core.tools import tool


@tool
def get_action_items(text: str) -> str:
    """Mock: Return fake action items content from text."""
    return "Action items content from the text (mocked)."
