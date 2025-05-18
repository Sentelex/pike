import pytest
from datetime import date, timedelta
from src.tools.stocks import get_stock_price


def test_get_stock_quote_valid_symbol():
    result = get_stock_price("AAPL")
    assert isinstance(result, dict)
    assert result["symbol"] == "AAPL"
    assert isinstance(result["price"], (int, float))


def test_get_stock_price_with_history():
    # Use a recent date range for reliable results
    end_date = date.today()
    start_date = end_date - timedelta(days=10)
    history = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "interval": "1d"
    }
    result = get_stock_price("AAPL", history=history)
    assert isinstance(result, dict)
    assert result["symbol"] == "AAPL"
    assert "history" in result
    assert "price" in result
    # The history field should not be empty
    assert history["start_date"] in result["history"]
    assert history["end_date"] in result["history"]
