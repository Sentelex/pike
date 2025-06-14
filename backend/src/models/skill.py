import pydantic as pdc
import langchain_core.tools as lct
import uuid as u

PIKE_BASE_SKILL_UUID = u.UUID("d9b77bd1-939d-4e09-9cec-4e2fee3a6548")


class SkillMeta(pdc.BaseModel.__class__):
    _instances: dict[type["Skill"], "Skill"] = {}
    _collections: dict[str, set[type["Skill"]]] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            if "id" not in kwargs:
                instance.id = u.uuid5(PIKE_BASE_SKILL_UUID, instance.name)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @classmethod
    def add_to_collection(
        cls, collection_name: str, skill_classes: type["Skill"] | list[type["Skill"]]
    ) -> None:
        """Add one or more skill classes to a named collection"""
        if collection_name not in cls._collections:
            cls._collections[collection_name] = set()

        if isinstance(skill_classes, list):
            cls._collections[collection_name].update(skill_classes)
        else:
            cls._collections[collection_name].add(skill_classes)

    @classmethod
    def get_collection(cls, collection_name: str) -> list["Skill"]:
        """Get all skill instances from a named collection"""
        if collection_name not in cls._collections:
            return []
        return [
            cls._instances[skill_class]
            for skill_class in cls._collections[collection_name]
        ]


class Skill(pdc.BaseModel, metaclass=SkillMeta):
    name: str
    description: str
    icon: str
    id: u.UUID | None = None
    tool: lct.StructuredTool

    @classmethod
    def get_all_skills(cls) -> list["Skill"]:
        """Get all instantiated skills"""
        return list(SkillMeta._instances.values())

    @classmethod
    def get_collection(cls, collection_name: str) -> list["Skill"]:
        """Get all skills from a named collection"""
        return SkillMeta.get_collection(collection_name)


class SkillInterface(pdc.BaseModel):
    id: u.UUID
    name: str
    description: str
    icon: str
