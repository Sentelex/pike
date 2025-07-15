import backend.src.pike_tool as pt


@pt.pike_tool(display="Parse Text File", icon="text-page-svgrepo-com.svg")
def parse_file(file: str) -> str:
    """Mock: Return fake parsed content from text file."""
    return "Parsed content from the text file (mocked)."
