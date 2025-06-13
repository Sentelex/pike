from pydantic import BaseModel, Field
from typing import Dict, Optional
import uuid
import os
from dotenv import load_dotenv
import langchain_google_genai as lcg
import langchain_openai as loai

load_dotenv()

# Environment variable setup
google_api_key = os.getenv("GOOGLE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
else:
    os.environ["OPENAI_API_KEY"] = ""

# Global cache for model instances
global MODEL_CACHE
MODEL_CACHE: dict[str, 'Model'] = {}


class Model(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    provider: str
    api_key: str
    additional_kwargs: Optional[Dict] = {}
    model_instance: object = None

    def model_post_init(self, __context: Optional[dict] = None) -> None:
        """
        Post-initialization method that creates the model instance and adds to cache.
        """
        global MODEL_CACHE

        # Set environment variables for model APIs
        if self.provider.lower() == "google":
            os.environ["GOOGLE_API_KEY"] = self.api_key
            # Create Google model instance
            self.model_instance = lcg.ChatGoogleGenerativeAI(
                model=self.name,
                google_api_key=self.api_key,
                **self.additional_kwargs
            )
        elif self.provider.lower() == "openai":
            os.environ["OPENAI_API_KEY"] = self.api_key
            # Create OpenAI model instance
            self.model_instance = loai.ChatOpenAI(
                model=self.name,
                **self.additional_kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        # Add to global cache
        MODEL_CACHE[self.id] = self


def get_default_model():
    provider = os.getenv("DEFAULT_MODEL_PROVIDER")
    if provider == "google":
        return Model(
            provider="google",
            name="gemini-2.0-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            additional_kwargs={}
        )
    elif provider == "openai":
        return Model(
            provider="openai",
            name="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            additional_kwargs={}
        )
    else:
        raise ValueError(f"Unsupported DEFAULT_MODEL_PROVIDER: {provider}")
