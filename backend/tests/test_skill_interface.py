import pytest
import json
import src.graph_builder as gb
import src.skill_interface as si


def test_get_available_skills_real():
    if not gb.SKILL_LOOKUP:
        pytest.skip("Skipping test because SKILL_LOOKUP is empty")

    response = si.get_available_skills()

    result = json.loads(response.body)

    assert isinstance(result, list)
    for tool in result:
        assert isinstance(tool, dict)
        assert "name" in tool
        assert "description" in tool
        assert "id" in tool
        assert "icon" in tool