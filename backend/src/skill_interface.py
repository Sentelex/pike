from fastapi.responses import JSONResponse
import src.graph_builder as gb
from typing import List
from src.models.skill import SkillInterface 


def get_available_skills():
    skills: List[SkillInterface] = [
        SkillInterface(
            name=t.name,
            description=t.description,
            id=t.metadata["uuid"],
            icon=t.metadata["icon"]
        ) for t in gb.SKILL_LOOKUP.values()
    ]

    response_data = [
        {**skill.model_dump()}
        for skill in skills
    ]

    return JSONResponse(content=response_data)
