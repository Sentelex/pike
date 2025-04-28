import langchain_core.tools as lcct


@lcct.tool
def parse_pdf(file: str) -> str:
    """Mock: Return fake parsed content from PDF."""
    return "Parsed content from the PDF (mocked)."
