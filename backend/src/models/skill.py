import pydantic as pdc
import langchain_core.tools as lct
import uuid as u

PIKE_BASE_SKILL_UUID = u.UUID("d9b77bd1-939d-4e09-9cec-4e2fee3a6548")


class SkillMeta(pdc.BaseModel.__class__):
    _instances: dict[str, "Skill"] = {}
    _collections: dict[str, set["Skill"]] = {}

    def __call__(cls, *args, **kwargs):
        if "name" not in cls.__annotations__:
            raise ValueError(f"Skill {cls} must define a 'name' field.")
        # Create a temporary instance to get the default value
        temp_instance = super().__call__(*args, **kwargs)
        new_name = temp_instance.name

        if new_name in cls._instances:
            raise ValueError(f"Skill with name '{new_name}' already exists")
        
        if "id" not in kwargs:
            temp_instance.id = u.uuid5(PIKE_BASE_SKILL_UUID, new_name)

        cls._instances[new_name] = temp_instance
        return temp_instance

    @classmethod
    def store_collection(
        cls, collection_name: str, skill_names: list[str]) -> bool:
        """Add one or more skills to a named collection by their names.
        
        Args:
            collection_name: The name associated with the stored skill collection.
            skill_names: A list of skill names to add to the collection.

        Returns:
            A dictionary mapping skill names to their instances in the collection.
        """
        if len(skill_names) == 0:
            return {}
        if collection_name in cls._collections:
            raise ValueError(f"The collection named '{collection_name}' already exists.")
        
        def add_skill_or_raise_error(name: str):
            if name not in cls._instances:
                raise ValueError(f"Skill with name '{name}' not found for collection '{collection_name}'")
            return cls._instances[name]
        
    
        named_skills = [add_skill_or_raise_error(name) for name in skill_names]
        cls._collections[collection_name] = set(named_skills)
        return True # Successfully stored the collection


    @classmethod
    def get_collection(cls, collection_name: str) -> None | list["Skill"]:
        """Get all skill instances from a named collection"""
        if collection_name not in cls._collections:
            return None
        return cls._collections[collection_name]
    

    @classmethod
    def get_all_skills(cls) -> list["Skill"]:
        """Get all instantiated skills"""
        return list(cls._instances.values())


class Skill(pdc.BaseModel, metaclass=SkillMeta):
    model_config = pdc.ConfigDict(arbitrary_types_allowed=True)

    name: str
    description: str
    icon: str
    id: u.UUID | None = None
    tool: lct.StructuredTool

    def __hash__(self):
        """Hash based on the skill's id only"""
        return hash(self.id)
    
    def model_dump(self, **kwargs):
        """Custom serialization method that handles both JSON and Python modes"""
        # Create a dict with only the serializable fields
        data = {
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            "id": str(self.id),
        }
        
        if kwargs.get("mode") == "json":
            return data
        
        data["tool"] = f"<StructuredTool: {self.tool.name}>"
        return data

class SkillInterface(pdc.BaseModel):
    id: u.UUID
    name: str
    description: str
    icon: str
