import uuid
import src.utils as ut


@ut.tool_with_metadata(
    name="File Parser",
    metadata={
            "uuid": str(uuid.uuid4()),
            "icon": "https://plus.unsplash.com/premium_photo-1677401495278-8c7fffe00792?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZmlsZSUyMGljb258ZW58MHx8MHx8fDA%3D",
        }
)
def parse_file(file: str) -> str:
    """Mock: Return fake parsed content from text file."""
    return "Parsed content from the text file (mocked)."
