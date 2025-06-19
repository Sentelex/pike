import pytest
import json
import uuid as u
import src.models.skill_loader as sl
import fastapi.responses as far


def test_get_available_skills_real():
    available_skills = sl.load_skills()
    content=[skill.model_dump(mode="json") for skill in available_skills]
    response = far.JSONResponse(content=content)
    result = json.loads(response.body)

    assert isinstance(result, list)
    for skill in result:
        assert isinstance(skill, dict)
        assert "name" in skill
        assert skill.get("name") is not None
        assert "description" in skill
        assert "id" in skill
        assert skill.get("id") is not None
        assert "icon" in skill
        assert skill.get("icon") is not None

def test_skills_have_callable_tools():
    available_skills = sl.load_skills()
    tool_list = {skill.name:skill.tool for skill in available_skills}
    for k,v in tool_list.items():
        assert k == v.name
        assert callable(v.func)