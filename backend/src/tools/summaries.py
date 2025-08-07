import src.pike_tool as pt
import pydantic as pdc


class SummarizeTextArgs(pdc.BaseModel):
    text: str = pdc.Field(
        description="Text from which a summary will be extracted."
    )


@pt.pike_tool(display="Summarize Text", 
              icon="flipped-book-svgrepo-com.svg",
              args_schema=SummarizeTextArgs)
def summarize_text(text: str) -> str:
    """Mock: Return a fake summary."""
    return "This is a summary of the text (mocked)."
