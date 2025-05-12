import langchain_core.tools as lcct


@lcct.tool
def get_action_items(text: str) -> str:
    """Mock: Return fake action items content from text."""
    return "Action items content from the text (mocked)."
