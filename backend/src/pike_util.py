import dotenv as de
import os

def extract_environ_var(var_name: str) -> str:
    extracted=None
    saved_env = dict(os.environ)
    try:
        de.load_dotenv()
        extracted = os.environ.get(var_name)
    finally:
        os.environ.clear()
        os.environ.update(saved_env)
    return extracted
