import os
import src.pike_util as pike_util

if os.environ.get("DEFAULT_MODEL_PROVIDER"):
    provider = os.environ.get("DEFAULT_MODEL_PROVIDER")
else:
    provider = pike_util.extract_environ_var("DEFAULT_MODEL_PROVIDER")

if os.environ.get("DEFAULT_DOMAIN"):
    domain = os.environ.get("DEFAULT_DOMAIN")
else:
    domain = pike_util.extract_environ_var("DEFAULT_DOMAIN")