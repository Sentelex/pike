from pydantic import BaseModel, Field
from typing import Dict
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class ModelInterface(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model_name: str
    provider: str
    api_key: str
    additional_kwargs: Dict
