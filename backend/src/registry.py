import src.tools as tools
import uuid

toolset = [
    {
        "tool": tools.get_action_items,
        "uuid": str(uuid.uuid4()),
        "icon": "https://images.unsplash.com/photo-1662027008658-b615840c7deb?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dG9kbyUyMGljb258ZW58MHx8MHx8fDA%3D",
    },
    {
        "tool": tools.parse_pdf,
        "uuid": str(uuid.uuid4()),
        "icon": "https://plus.unsplash.com/premium_photo-1677723530050-a1b18109fdd0?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8cGRmJTIwaWNvbnxlbnwwfHwwfHx8MA%3D%3D",
    },
    {
        "tool": tools.get_stock_price,
        "uuid": str(uuid.uuid4()),
        "icon": "https://plus.unsplash.com/premium_photo-1683583961436-fa9efb9f72d7?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8c3RvY2slMjBwcmljZSUyMGljb258ZW58MHx8MHx8fDA%3D",
    },
    {
        "tool": tools.parse_file,
        "uuid": str(uuid.uuid4()),
        "icon": "https://plus.unsplash.com/premium_photo-1677401495278-8c7fffe00792?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZmlsZSUyMGljb258ZW58MHx8MHx8fDA%3D",
    },
    {
        "tool": tools.parse_webpage,
        "uuid": str(uuid.uuid4()),
        "icon": "https://plus.unsplash.com/premium_photo-1685086785230-2233cf5d8f28?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8d2Vic2l0ZSUyMGljb258ZW58MHx8MHx8fDA%3D",
    },
    {
        "tool": tools.summarize_text,
        "uuid": str(uuid.uuid4()),
        "icon": "https://images.unsplash.com/photo-1705490020987-b4565b36c04d?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHN1bW1hcml6ZXIlMjBpY29ufGVufDB8fDB8fHww",
    },
]

AGENT_LOOKUP = {
    "default": [tool["tool"].name for tool in toolset],
}
SKILL_LOOKUP = {tool["tool"].name: tool for tool in toolset}
