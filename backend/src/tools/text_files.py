import langchain_core.tools as lcct
from ..models import skill as sk


class TextParserSkill(sk.Skill):
    def __init__(self):
        super().__init__(
            name="File Parser",
            description="Parse and return the content of a text file",
            icon="📝",
            tool=lcct.StructuredTool.from_function(
                func=self.parse_file,
                name="File Parser",
                description="Parse and return the content of a text file",
            ),
        )

    def parse_file(self, file: str) -> str:
        """Mock: Return fake parsed content from text file."""
        return "Parsed content from the text file (mocked)."
