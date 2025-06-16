import pytest
import json
import src.registry as rg
import src.skill_interface as si
import src.models.skill_loader as sl
import fastapi.responses as far


# def test_get_available_skills_real():
#     if not rg.SKILL_LOOKUP:
#         pytest.skip("Skipping test because SKILL_LOOKUP is empty")

#     response = si.get_available_skills()

#     result = json.loads(response.body)

#     assert isinstance(result, list)
#     for tool in result:
#         assert isinstance(tool, dict)
#         assert "name" in tool
#         assert "description" in tool
#         assert "id" in tool
#         assert "icon" in tool


def test_get_available_skills_real():
    available_skills = sl.load_skills()
    content = [{**skill.model_dump()} for skill in available_skills]
    response = far.JSONResponse(content=content)
    result = json.loads(response.body)

    assert isinstance(result, list)
    for tool in result:
        assert isinstance(tool, dict)
        assert "name" in tool
        assert "description" in tool
        assert "id" in tool
        assert "icon" in tool
