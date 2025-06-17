import pytest
import json
import src.registry as rg
import src.skill_interface as si
import src.models.skill_loader as sl
import fastapi.responses as far


def test_get_available_skills_real():
    available_skills = sl.load_skills()
    content=[skill.model_dump(mode="json") for skill in available_skills]
    response = far.JSONResponse(content=content)
    result = json.loads(response.body)

    assert isinstance(result, list)
    for tool in result:
        assert isinstance(tool, dict)
        assert "name" in tool
        assert "description" in tool
        assert "id" in tool
        assert "icon" in tool

def test_skills_have_callable_tools():
    available_skills = sl.load_skills()
    tool_list = {skill.name:skill.tool for skill in available_skills}
    for k,v in tool_list.items():
        assert k == v.name 
        assert callable(v.func)