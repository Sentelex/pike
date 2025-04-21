import langchain_core.tools as lcct
import yfinance as yf


@lcct.tool
def get_stock_price(stock_handle: str) -> str:
    """
    Fetches stock information using Yahoo Finance.

    Args:
        stock_handle (str): Stock ticker (e.g., "AAPL").

    Returns:
        dict: Stock data including price and metadata.

    Raises:
        ValueError: If symbol is invalid or data is unavailable.
        ConnectionError: If a network issue occurs.
    """
    try:
        ticker = yf.Ticker(stock_handle)
        data = ticker.info

        if not data or "regularMarketPrice" not in data:
            raise ValueError(f"Stock data not found for symbol '{stock_handle.upper()}'.")

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
        }

    except AttributeError as e:
        raise ValueError(f"Invalid ticker symbol '{stock_handle.upper()}' or bad response.") from e
    except Exception as e:
        raise ConnectionError(f"Failed to fetch stock data: {str(e)}") from e

