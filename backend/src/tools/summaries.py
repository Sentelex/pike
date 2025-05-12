import backend.src.pike_tool as pt
import google.generativeai as genai
from jinja2 import Environment, FileSystemLoader
import os
import json
from dotenv import load_dotenv


load_dotenv()

@pt.pike_tool(display="Summarize Text", icon="flipped-book-svgrepo-com.svg")
def summarize_text(input_text: str) -> str:
    """
    Summarize a given text using a language model and a Jinja2 prompt template.

    This function leverages Google's Gemini model to generate a dense summary
    of the provided input text. It loads a Jinja2 template to format the prompt
    and returns the model's summarized output.

    Parameters
    ----------
    input_text : str
        The text to be summarized.

    Returns
    -------
    str
        A concise summary of the input text, returned from the language model.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("templates/summarize.j2")

    prompt = template.render(input_text=input_text)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    response_text = response.text.strip().strip("`").replace("json", "", 1).strip()

    try:
        summary_data = json.loads(response_text)
        final_summary = summary_data[-1]["Denser_Summary"]
    except Exception as e:
        raise ValueError("Failed to parse summary response: " + str(e))

    return final_summary.strip()
