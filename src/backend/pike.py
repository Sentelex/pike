import contextlib as cl
import fastapi as fapi
import fastapi.middleware.cors as fapi_cors
import fastapi.security as fapi_sec
import typing as t
import pydantic as pyd


import test_data as teda
import data_maps as dm
import graph_builder as gb

model = "Some Model"
graph = gb.build_graph(model, graph_id="default")

def get_user_chat_map() -> dm.UserChat:
    """
    Get the user thread map storing the threads associated with each user.
  
    Returns
    -------
    dict
        Dictionary mapping UserToken to list of ThreadIdentifiers.
    """
    # This is a placeholder function. In a real application, this would fetch
    # data from a database or other storage.
    return teda.user_chat_map


user_map = {}

@cl.asynccontextmanager
async def service_lifecycle(app: fapi.FastAPI):
    """
    Lifecycle context manager for FastAPI app.

    Parameters
    ----------
    app : fapi.FastAPI
        FastAPI app instance.

    Yields
    ------
    None
    """
    # Should we actually have a server singleton here to hold things like the
    #   user_map and other server state variables (database, )
    user_map = get_user_chat_map()
    # Startup: Initialize things that need to be in place before the backend starts
    # e.g. database connections, prefect initialization, etc.

    # Run the app:
    yield

    # Shutdown: Perform any cleanup tasks that need to be done before server shutdown
    # e.g. close database connections, stop background tasks, etc.

    # save_user_map(user_map) # For eventual use when we have a database
    del user_map
    
api = fapi.FastAPI(lifespan=service_lifecycle)
security = fapi_sec.HTTPBasic()

api.add_middleware(
    fapi_cors.CORSMiddleware,
    allow_origins=["http://localhost", "https://localhost", "https://localhost:8080"],
    # Should be restricted to designated front ends for production/testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

