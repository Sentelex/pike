import langchain_core.tools as lcct


@lcct.tool("File Parser")
def parse_file(file: str) -> str:
    """Mock: Return fake parsed content from text file."""
    return "Parsed content from the text file (mocked)."
