import langchain_core.tools as lcct
import yfinance as yf
import pandas as pd
from datetime import date
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@lcct.tool
def get_stock_price(stock_handle: str,
                    history: dict,) -> str:
    """
    Fetches stock information using Yahoo Finance.

    Args:
        stock_handle (str): Stock ticker (e.g., "AAPL").
        history (dict, optional): Dictionary for historical data query. Keys:
            - period (str, optional): Data period to download. Valid periods:
                "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max".
                Use either 'period' or 'start'/'end'.
            - interval (str, optional): Data interval. Valid intervals:
                "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo".
                Note: "1m" data is only available for the last 7 days, and intervals <1d for the last 60 days.
            - start_date (str, optional): Start date (yyyy-mm-dd) if not using 'period'.
            - end_date (str, optional): End date (yyyy-mm-dd) if not using 'period'.

    Returns:
        dict: Stock data including price, metadata, and historical data.

    Raises:
        ValueError: If symbol is invalid or data is unavailable.
        ConnectionError: If a network issue occurs.
    """
    ticker = yf.Ticker(stock_handle)
    data = ticker.info
    if history is not None:
        if history['end_date'] is None:
            history['end_date'] = date.today().strftime("%Y-%m-%d")
        history['end_date'] = pd.to_datetime(history['end_date'])
        history['end_date'] = history['end_date'].tz_localize(None)
        if history.get('period') is not None:
            h_data = ticker.history(period=history['period'],)
        else:
            h_data = ticker.history(
                start=history.get('start_date'),
                end=history.get('end_date'),
                period=history.get('interval'),
            )
            if len(h_data) > 100:
                logger.warning(
                    f"History data for {stock_handle} is too long, truncating to 100 rows."
                )
                h_data = h_data.iloc[-100:]
    else:
        h_data = None
    if not data or "regularMarketPrice" not in data:
        raise ValueError(
            f"Stock data not found for symbol '{stock_handle.upper()}'.")
    return {
        "symbol": stock_handle.upper(),
        "name": data.get("shortName", "N/A"),
        "price": data["regularMarketPrice"],
        "previous_close": data.get("regularMarketPreviousClose", "N/A"),
        "open": data.get("regularMarketOpen", "N/A"),
        "high": data.get("regularMarketDayHigh", "N/A"),
        "low": data.get("regularMarketDayLow", "N/A"),
        "volume": data.get("regularMarketVolume", "N/A"),
        "change": data.get("regularMarketChange", "N/A"),
        "percent_change": f"{data.get('regularMarketChangePercent', 0):.2f}%",
        "currency": data.get("currency", "USD"),
        "market_state": data.get("marketState", "N/A"),
        'history': h_data.to_json(),
    }
