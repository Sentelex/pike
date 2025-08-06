import backend.src.pike_tool as pt
import backend.src.model as ml
from jinja2 import Environment, FileSystemLoader
import os
import json
from dotenv import load_dotenv

load_dotenv()

@pt.pike_tool(display="Summarize Text", icon="flipped-book-svgrepo-com.svg")
def summarize_text(input_text: str, num: int=5) -> str:
    """
    Generate a concise summary of the given text.

    Parameters
    ----------
    input_text : str
        The text to summarize.
    num : int
        The number of iterations to generate the summary.

    Returns
    -------
    str
        A short, dense summary of the input.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY must be set in the environment")

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("templates/CoD_summarize.j2")
    prompt = template.render(num=num, input_text=input_text)

    # TODO:  Create a better way to do this -> pass model into tools which want models
    model = ml.Model(name="gemini-2.0-flash-lite", provider="google", api_key=api_key)
    response = model.model_instance.invoke(prompt)

    try:
        response_text = response.content.strip().strip("`").replace("json", "", 1).strip()
        summary_data = json.loads(response_text)
        return summary_data[-1]["Denser_Summary"].strip()
    except Exception as e:
        raise ValueError(f"Failed to parse summary response: {e}")
