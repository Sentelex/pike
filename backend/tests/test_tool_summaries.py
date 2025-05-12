import pytest
import json
from types import SimpleNamespace
from src.pike_tools import summaries as su


@pytest.fixture
def mock_dependencies(monkeypatch):
    # Capture the prompt sent to the model
    captured = {}

    # Mock genai.configure
    monkeypatch.setattr("src.pike_tools.summaries.genai.configure", lambda **kwargs: None)

    # Mock template rendering
    class MockTemplate:
        def render(self, input_text):
            assert isinstance(input_text, str)
            rendered_prompt = f"Summarize: {input_text}"
            captured['prompt'] = rendered_prompt
            return rendered_prompt

    class MockEnv:
        def get_template(self, name):
            assert name == "templates/summarize.j2"
            return MockTemplate()

    monkeypatch.setattr("src.pike_tools.summaries.Environment", lambda *args, **kwargs: MockEnv())

    # Mock Gemini model
    class MockModel:
        def generate_content(self, prompt):
            assert "Summarize:" in prompt
            # Return a fake JSON-like summary structure
            fake_json = [
                {"Missing_Entities": ["AI", "world"], "Denser_Summary": "AI is transforming the world."},
                {"Missing_Entities": ["technology"], "Denser_Summary": "AI and technology are transforming the world."}
            ]
            return SimpleNamespace(text=f"```json\n{json.dumps(fake_json)}\n```")

    monkeypatch.setattr("src.pike_tools.summaries.genai.GenerativeModel", lambda name: MockModel())

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
    print("\nReal summary output:", output)
