import langchain_core.tools as lcct


@lcct.tool
def parse_webpage(website: str) -> str:
    """Mock: Return fake parsed content from website."""
    return "Parsed content from the website (mocked)."
