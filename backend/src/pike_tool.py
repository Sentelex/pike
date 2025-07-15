import langchain_core.tools as lct
import langchain_core.runnables as lcr
import typing as t
import backend.src.model as bm
import base64
import urllib
import os
import importlib as il
import dotenv as de
import uuid as u


def get_icons_path() -> str:
    tools_path = il.resources.files("backend.src.tools")
    icons_path = tools_path / "icons"
    return icons_path

def pad_base64(input_str: str) -> str:
    missing_padding = len(input_str) % 4
    if missing_padding:
        input_str += '=' * (4-missing_padding)
    return input_str

def encode_icon_url_safe_utf8(icon_name: str) -> str:
    """Encodes binary icon svg file to a URL-safe UTF-8 string."""
    icon_path = os.path.join(get_icons_path(), icon_name)
    with open(icon_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        url_safe_string = urllib.parse.quote(encoded_string, safe="")
        return pad_base64(urllib.parse.unquote(url_safe_string))

class PikeTool(lct.BaseTool):
    """
    Extended BaseTool with icon and optional LLM model.
    If the tool function requires an LLM, it will be passed as an argument.
    """
    icon: str | None = None  # base64-encoded icon
    llm: bm.Model | None = None
    id: u.UUID | None = None
    func: t.Callable 

    def __init__(
        self,
        name: str,
        display: str,
        description: str,
        func: t.Callable,
        icon: str | None = None,
        llm: bm.Model | None = None,
        args_schema: lct.ArgsSchema | None = None,
        return_direct: bool = False,
        **kwargs
    ):
        super().__init__(
            display=display,
            name=name,
            description=description,
            func=func,
            args_schema=args_schema,
            return_direct=return_direct,
            **kwargs
        )

        self.func = func
        self.icon = encode_icon_url_safe_utf8(icon or "pike_default_icon.svg")
        self.llm = llm

    def model_post_init(self, __context=None):
        orig_env = os.environ.copy()
        de.load_dotenv()  # TODO: Replace with a config method that doesn't clobber the environment.
        DEFAULT_DOMAIN = os.getenv("DEFAULT_DOMAIN", "nothing.nowhere.com")
        os.environ.clear()
        os.environ.update(orig_env)
        self.id = u.uuid5(u.uuid5(u.NAMESPACE_DNS, DEFAULT_DOMAIN), self.name)

    def _call(self, *args, **kwargs):
        """
        Calls the tool function, passing the LLM if present and required.
        """
        import inspect

        sig = inspect.signature(self.func)
        if self.llm is not None and 'llm' in sig.parameters:

            return self.func(*args, llm=self.llm, **kwargs)
        else:
            return self.func(*args, **kwargs)
        
    def _run(self, *args, **kwargs):
        """
        Runs the tool function with the provided arguments.
        This method is called by the LangChain framework.
        """
        return self._call(*args, **kwargs)

# langchain_core.tools.tool() call cases:
#   1. name_or_callable = None, runnable=None
#   2. name_or_callable = str (name), runnable = Runnable
#   3. name_or_callable = callable (func), runnable = None
#   4. name_or_callable = str(name), runnable = None
#
#   If runnable: (Case 2)
#     if no name_or_callable: RaiseError
#     if name_or_callable is not str:  Raise error
#     return tool(name_or_callable)(runnable)

#   If name_or_callable not none: (Case 3 or 4)
#     if name_or_callable is callable:
#       # Got a function
#       func = name_or_callable
#       return tool(name=func.__name__)(func)
#     elif name_or_callable is str:
#       return tool(name=name_or_callable)
#     else:
#       raise BadArgumentError(Need name or callable with .__name__)

#    Case 1:  Calling a decorator on a function/runnable to add info, but not
#             redefine required arguments
#    Define partial by extracting name from runnable or func
#    def _partial(func: t.Callable | langchain_core.runnagles.Runnable) -> BaseTool:
#        return 


def pike_tool(
    func: t.Callable | None = None,
    runnable: lcr.Runnable | None = None,
    *,
    display: str | None = None,
    name: str | None = None,
    description: str | None = None,
    icon: str | None = None,
    llm: bm.Model | None = None,
    args_schema: lct.ArgsSchema | None = None,
    return_direct: bool = False,
):
    """
    Decorator to create a PikeTool from a function.
    Usage:
        @pike_tool(description="Echo tool", icon="myicon.svg", llm=my_llm)
        def echo(text: str): ...
    """
    def decorator(func):
        tool_name = name or func.__name__
        display_text = display or tool_name
        tool_description = description or func.__doc__ or ""
        return PikeTool(
            display=display_text,
            name=tool_name,
            description=tool_description,
            func=func,
            icon=icon,
            llm=llm,
            args_schema=args_schema,
            return_direct=return_direct,
        )
    if func is None:
        return decorator
    else:
        return decorator(func)
