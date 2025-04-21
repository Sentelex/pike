import pytest
from src.tools.stocks import get_stock_price


def test_get_stock_quote_valid_symbol():
    result = get_stock_price("AAPL")
    assert isinstance(result, dict)
    assert result["symbol"] == "AAPL"
    assert isinstance(result["price"], (int, float))


def test_get_stock_quote_invalid_symbol():
    with pytest.raises(ValueError, match="Invalid ticker symbol 'INVALIDSYM' or bad response."):
        get_stock_price("INVALIDSYM")


def test_get_stock_quote_network_failure(monkeypatch):
    def mock_info_failure(*args, **kwargs):
        raise Exception("Mock network error")

    monkeypatch.setattr("yfinance.Ticker.info", property(mock_info_failure))

    with pytest.raises(ConnectionError, match="Mock network error"):
        get_stock_price("AAPL")
