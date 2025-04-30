import contextlib as cl
import fastapi as fapi
import fastapi.middleware.cors as fapi_cors

import src.graph_builder as gb

model = "Some Model"
graph = gb.build_graph(model, graph_id="default")


@cl.asynccontextmanager
def service_lifecycle(app: fapi.FastAPI):
    """
    Lifecycle context manager for FastAPI app.
    """

    ## Do pre-app run setup stuff here
    # Startup: Initialize things that need to be in place before the backend starts
    # e.g. database connections, prefect initialization, etc.

    ##### e.g. load data, init databases, etc..

    # Run the app:
    yield

    ## Do the post-app run shutdown stuff here
    # Shutdown: Perform any cleanup tasks that need to be done before server shutdown
    # e.g. close database connections, stop background tasks, etc.

    ##### e.g. save data, shutdown databases, etc..


api = fapi.FastAPI(lifespan=service_lifecycle)

api.add_middleware(
    fapi_cors.CORSMiddleware,
    allow_origins=["http://localhost", "https://localhost", "https://localhost:8080"],
    # Should be restricted to designated front ends for production/testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=8000)
