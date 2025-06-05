import langchain_core.tools as lcct
from langchain_google_genai import ChatGoogleGenerativeAI
from jinja2 import Environment, FileSystemLoader
import os
import json
from dotenv import load_dotenv

load_dotenv()

@lcct.tool
def summarize_text(input_text: str) -> str:
    """
    Generate a concise summary of the given text.

    Parameters
    ----------
    input_text : str
        The text to summarize.

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
    prompt = template.render(input_text=input_text)

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
    response = model.invoke(prompt)

    try:
        response_text = response.content.strip().strip("`").replace("json", "", 1).strip()
        summary_data = json.loads(response_text)
        return summary_data[-1]["Denser_Summary"].strip()
    except Exception as e:
        raise ValueError(f"Failed to parse summary response: {e}")
