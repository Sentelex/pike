import pytest
import json
from types import SimpleNamespace
from backend.src.tools import summaries as su


@pytest.fixture
def mock_dependencies(monkeypatch):
    # Capture the prompt sent to the model
    captured = {}

    # Mock LangChain ChatGoogleGenerativeAI
    class MockModel:
        def invoke(self, prompt):
            assert "Summarize:" in prompt
            captured['prompt'] = prompt
            fake_json = [
                {"Missing_Entities": ["AI", "world"], "Denser_Summary": "AI is transforming the world."},
                {"Missing_Entities": ["technology"], "Denser_Summary": "AI and technology are transforming the world."}
            ]
            return SimpleNamespace(content=f"```json\n{json.dumps(fake_json)}\n```")

    # Patch model initialization to use MockModel
    def mock_post_init(self, *args, **kwargs):
        self.model_instance = MockModel()

    monkeypatch.setattr("backend.src.model.Model.model_post_init", mock_post_init)

    # Patch Jinja environment and rendering
    class MockTemplate:
        def render(self, num, input_text):
            rendered = f"Summarize: {input_text}"
            return rendered

    class MockEnv:
        def get_template(self, name):
            assert name == "templates/CoD_summarize.j2"
            return MockTemplate()

    monkeypatch.setattr("backend.src.tools.summaries.Environment", lambda *args, **kwargs: MockEnv())

    return captured


def test_summarize_text_mocked(mock_dependencies):
    input_text = "Artificial Intelligence is transforming the world."
    output = su.summarize_text(input_text)

    expected_prompt = f"Summarize: {input_text}"
    assert mock_dependencies['prompt'] == expected_prompt
    assert output == "AI and technology are transforming the world."


# --- Optional test with real Gemini model, skipped in CI ---
@pytest.mark.skip_in_pipeline
def test_summarize_text_real():
    input_text = "Artificial Intelligence is changing global industries with automation, data analysis, and decision-making support."
    output = su.summarize_text(input_text)

    assert isinstance(output, str)
