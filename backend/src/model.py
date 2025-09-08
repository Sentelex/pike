from pydantic import BaseModel, Field
from typing import Dict, Optional
import uuid
import os
from dotenv import load_dotenv
import langchain_google_genai as lgai
import langchain_openai as loai
import langchain_core.runnables as lcr
import src.pike_util as pike_util

# Global cache for model instances
global MODEL_CACHE
MODEL_CACHE: dict[str, 'Model'] = {}


class Model(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    provider: str
    additional_kwargs: Optional[Dict] = {}
    model_instance: object = None

    def model_post_init(self, __context: Optional[dict] = None) -> None:
        """
        Pydantic model post-initialization method that creates the model 
        instance and adds it to cache.
        """
        global MODEL_CACHE

        # Instantiate provider models without embedding API keys in environment.
        if self.provider.lower() == "google":
            # Create Google model instance
            raw_model = lgai.ChatGoogleGenerativeAI(
                model=self.name,
                google_api_key=pike_util.extract_environ_var("GOOGLE_API_KEY"),
                **self.additional_kwargs
            )
        elif self.provider.lower() == "openai":
            # Create OpenAI model instance
            raw_model = loai.ChatOpenAI(
                model=self.name,
                api_key=pike_util.extract_environ_var("OPENAI_API_KEY"),
                **self.additional_kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        # Seem to be having some initialization issues, so let's add a small
        #   retry queue to the model for robustness
        self.model_instance = raw_model
        MODEL_CACHE[self.id] = self


def create_default_model():
    provider = os.getenv("DEFAULT_MODEL_PROVIDER")
    if provider == "google":
        return Model(
            provider="google",
            name="gemini-2.0-flash",
            api_key=pike_util.extract_environ_var("GOOGLE_API_KEY"),
            additional_kwargs={}
        )
    elif provider == "openai":
        return Model(
            provider="openai",
            name="gpt-4o-mini",
            api_key=pike_util.extract_environ_var("OPENAI_API_KEY"),
            additional_kwargs={}
        )
    else:
        raise ValueError(f"Unsupported DEFAULT_MODEL_PROVIDER: {provider}")

def get_default_model():
    global MODEL_CACHE
    if not "default" in MODEL_CACHE:
        MODEL_CACHE["default"] = create_default_model()
    return MODEL_CACHE["default"]

