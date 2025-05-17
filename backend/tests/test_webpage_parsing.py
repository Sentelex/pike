import os
import pytest
import requests
import src.tools.web_pages as wp

TEST_PAGE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './test_page.html'))

@pytest.fixture
def local_test_page_url():
    # Use file:// URL for local HTML file
    return f'file://{TEST_PAGE_PATH}'

@pytest.fixture
def patch_requests_get_local_file(monkeypatch):
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

def test_parse_webpage_returns_all_test_texts(local_test_page_url, patch_requests_get_local_file):
    # Patch requests.get to read the local file instead of making an HTTP request
    result = wp.parse_webpage(local_test_page_url)
    for i in range(1, 12):
        assert f'Test_Text_{i}' in result, f"Test_Text_{i} not found in parsed content"

def test_parse_webpage_ignores_scripts(local_test_page_url, patch_requests_get_local_file):
    # Patch requests.get to read the local file instead of making an HTTP request
    result = wp.parse_webpage(local_test_page_url)
    assert 'Test_Text_12' not in result, f"Test_Text_12 should not be found in parsed content"

def test_parse_webpage_raises_for_nonexistent_url():
    non_existent_url = 'http://localhost:9999/thispagedoesnotexist.html'
    with pytest.raises(Exception):
        wp.parse_webpage(non_existent_url)
