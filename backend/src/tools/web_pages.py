import uuid
import src.utils as ut


@ut.tool_with_metadata(
    name="Webpage Parser",
    metadata={
            "uuid": str(uuid.uuid4()),
            "icon": "https://plus.unsplash.com/premium_photo-1685086785230-2233cf5d8f28?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8d2Vic2l0ZSUyMGljb258ZW58MHx8MHx8fDA%3D",
        }
)
def parse_webpage(website: str) -> str:
    """Mock: Return fake parsed content from website."""
    return "Parsed content from the website (mocked)."
