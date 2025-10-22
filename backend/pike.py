import contextlib as cl
import fastapi as fapi
import fastapi.middleware.cors as fapi_cors
import routes as routes


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
