from langchain_core.tools import tool


@tool
def get_stock_price(stock_handle: str) -> str:
    """Mock: Return fake stock price info."""
    return f"The stock price of {stock_handle} is $420.42 (mocked)."
