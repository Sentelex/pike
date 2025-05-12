import src.pike_tool as pt
import pydantic as pdc


class ParseFileArgs(pdc.BaseModel):
    file: str = pdc.Field(
        description="Text file to extract data from.")

@pt.pike_tool(display="Parse Text File", 
              icon="text-page-svgrepo-com.svg",
              args_schema=ParseFileArgs)
def parse_file(file: str) -> str:
    """Mock: Return fake parsed content from text file."""
    return "Parsed content from the text file (mocked)."
