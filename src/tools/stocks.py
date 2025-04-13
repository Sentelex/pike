from langchain_core.tools import tool

@tool
def get_stock_price(stockhandle: str) -> str:
    """Mock: Return fake stock price info."""
    return f"The stock price of {stockhandle} is $420.42 (mocked)."
