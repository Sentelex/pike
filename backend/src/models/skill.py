from pydantic import BaseModel, Field
import uuid


class SkillInterface(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
