import os
import pytest
import requests
import src.tools.web_pages as wp
import pydantic as pyd

@pytest.fixture
def local_test_page_url():
    # Use file:// URL for local HTML file
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), './test_page.html'))
    return f'file://{path}'

@pytest.fixture
def patch_requests_get_local_file(monkeypatch):
    """
    Patch requests.get to read a local file instead of making an HTTP request.
    """
    class DummyResponse:
        def __init__(self, content):
            self.content = content
        def raise_for_status(self):
            pass

    def dummy_get(url, *args, **kwargs):
        if url.startswith('file://'):
            with open(url[7:], 'rb') as f:
                return DummyResponse(f.read())
        return requests.get(url, *args, **kwargs)
    monkeypatch.setattr(requests, 'get', dummy_get)

@pytest.fixture
def patch_anyhttpurl_accepts_file(monkeypatch):
    """
    Patch pydantic.AnyHttpUrl to accept file:// URLs for testing purposes.
    """
    class PatchedAnyHttpUrl(str):
        @classmethod
        def __get_validators__(cls):
            def validator(value):
                if value.startswith("file://") or value.startswith("http://") or value.startswith("https://"):
                    return value
                raise ValueError("URL scheme should be 'http', 'https', or 'file'")
            yield validator
    monkeypatch.setattr(pyd, 'AnyHttpUrl', PatchedAnyHttpUrl)

def test_parse_webpage_returns_all_test_texts(
        local_test_page_url, 
        patch_requests_get_local_file, 
        patch_anyhttpurl_accepts_file
):
    # Patch requests.get to read the local file instead of making an HTTP request
    result = wp.parse_webpage(local_test_page_url)
    test_texts = [f'Test_Text_{i}' for i in range(1, 12)] # List of texts expected to be extracted from test_page.html
    for text in test_texts:
        assert text in result, f"{text} not found in parsed content"

def test_parse_webpage_ignores_scripts(
        local_test_page_url, 
        patch_requests_get_local_file,
        patch_anyhttpurl_accepts_file
):
    # Patch requests.get to read the local file instead of making an HTTP request
    result = wp.parse_webpage(local_test_page_url)
    assert 'Test_Text_12' not in result, f"Test_Text_12 should not be found in parsed content"

def test_parse_webpage_raises_for_nonexistent_url():
    non_existent_url = 'http://localhost:9999/thispagedoesnotexist.html'
    with pytest.raises(requests.HTTPError):
        wp.parse_webpage(non_existent_url)

def test_parse_webpage_raises_for_wrong_url_scheme():
    wrong_url = 'ftp://example.com/test_page.html'
    with pytest.raises(pyd.ValidationError):
        wp.parse_webpage(wrong_url)

def test_parse_webpage_raises_for_unsanitizable_url():
    unsanitizable_url = 'file://path-only'
    with pytest.raises(pyd.ValidationError):
        wp.parse_webpage(unsanitizable_url)
