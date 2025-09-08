import contextlib as cl
import fastapi as fapi
import fastapi.middleware.cors as fapi_cors
import routes as routes
import dotenv as de
import src.pike_util as pike_util
import os



if not os.environ.get("DEFAULT_MODEL_PROVIDER"):
    default_provider = pike_util.extract_environ_var("DEFAULT_MODEL_PROVIDER")
    os.environ["DEFAULT_MODEL_PROVIDER"]=default_provider

if not os.environ.get("DEFAULT_DOMAIN"):
    default_domain = pike_util.extract_environ_var("DEFAULT_DOMAIN")
    os.environ["DEFAULT_DOMAIN"]=default_domain

@cl.asynccontextmanager
async def service_lifecycle(app: fapi.FastAPI):
    """
    Lifecycle context manager for FastAPI app.
    """

    # Do pre-app run setup stuff here
    yield
    # Do the post-app run shutdown stuff here


api = fapi.FastAPI(lifespan=service_lifecycle)
api.include_router(routes.pike_router)

api.add_middleware(
    fapi_cors.CORSMiddleware,
    allow_origins=["http://localhost",
                   "https://localhost", "http://localhost:8080"],
    # Should be restricted to designated front ends for production/testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=8000)
