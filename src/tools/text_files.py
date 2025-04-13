from langchain_core.tools import tool

@tool
def parse_file(file: str) -> str:
    """Mock: Return fake parsed content from text file."""
    return "Parsed content from the text file (mocked)."
