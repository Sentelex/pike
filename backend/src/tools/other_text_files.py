import langchain_core.tools as lcct
from ..models import icon_process as ip
from ..models import skill as sk

#  Candidate Icon:
#  https://plus.unsplash.com/premium_photo-1677401495278-8c7fffe00792?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZmlsZSUyMGljb258ZW58MHx8MHx8fDA%3D

class AltTextParserSkill(sk.Skill):
    name: str = "Other File Parser"
    description: str = "Parse and return the content of an other text file"
    icon: str = ip.encode_icon_url_safe_utf8("text-page-svgrepo-com.svg")

    @lcct.tool(name.replace(" ","_"))
    def parse_file(self, file: str) -> str:
        """Mock: Return other fake parsed content from text file."""
        return "Parsed content from the other text file (mocked)."

    tool: lcct.Tool = parse_file
