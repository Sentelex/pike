import backend.src.pike_tool as pt


@pt.pike_tool(display="Get Stock Price", icon="stock-svgrepo-com.svg")
def get_stock_price(stock_handle: str) -> str:
    """Mock: Return fake stock price info."""
    return f"The stock price of {stock_handle} is $420.42 (mocked)."
