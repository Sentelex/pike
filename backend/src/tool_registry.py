import src.tools as tools

toolset = [
    tools.get_action_items,
    tools.parse_pdf,
    tools.get_stock_price,
    tools.parse_file,
    tools.parse_webpage,
    tools.summarize_text,
]

AGENT_LOOKUP = {
    "default": [tool.name for tool in toolset],
}
SKILL_LOOKUP = {tool.name: tool for tool in toolset}
