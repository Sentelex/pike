import langchain_core.tools as lcct
from ..models import skill as sk


class TextParserSkill(sk.Skill):
    name: str = "Other File Parser"
    description: str = "Parse and return the content of a text file"
    icon: str = "📝"

    def parse_file(self, file: str) -> str:
        """Mock: Return other fake parsed content from text file."""
        return "Parsed content from the other text file (mocked)."

    tool: lcct.Tool = lcct.tool("Other File Parser")(parse_file)
