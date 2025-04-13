from langchain_core.tools import tool

@tool
def parse_webpage(website: str) -> str:
    """Mock: Return fake parsed content from website."""
    return "Parsed content from the website (mocked)."
