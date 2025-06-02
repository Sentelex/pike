from pydantic import BaseModel, Field
from typing import Dict
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class ModelInterface(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model_name: str = "gemini"
    provider: str = "Google"
    api_key: str = os.getenv("GOOGLE_API_KEY")
    additional_kwargs: Dict = Field(default_factory=lambda: {
        "temperature": 0.7,
        "max_tokens": 1024
    })
