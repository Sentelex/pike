from fastapi.responses import JSONResponse
import src.graph_builder as gb
import src.registry as rg
from typing import List
from src.models.skill import SkillInterface 


def get_available_skills():
    skills: List[SkillInterface] = [
        SkillInterface(
            name=t["tool"].name,
            description=t["tool"].description,
            id=t["uuid"],
            icon=t["icon"]
        ) for t in rg.SKILL_LOOKUP.values()
    ]

    response_data = [
        {**skill.model_dump()}
        for skill in skills
    ]

    return JSONResponse(content=response_data)
