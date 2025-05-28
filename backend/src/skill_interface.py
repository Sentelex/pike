from fastapi.responses import JSONResponse
import src.graph_builder as gb


def get_available_skills():
    skills = [
        {
            "name": t.name,
            "description": t.description,
            "id": t.metadata["uuid"],
            "icon": t.metadata["icon"]
        } for t in gb.SKILL_LOOKUP.values()
    ]
    return JSONResponse(content=skills)
