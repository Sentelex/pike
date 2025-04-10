import jinja2
from pathlib import Path

class LLMOrchestrater:
    def __init__(self, prompt_path="prompts/router_prompt.jinja"):
        self.template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=Path(prompt_path).parent)
        ).get_template(Path(prompt_path).name)

    def render_prompt(self, short_state):
        return self.template.render(state=short_state)

    def get_response(self, short_state):
        prompt = self.render_prompt(short_state)
        # Here you would pass the prompt to the actual LLM : chat, tools
        return "LLM response based on prompt"
