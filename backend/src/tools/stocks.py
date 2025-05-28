import uuid
import src.utils as ut


@ut.tool_with_metadata(
    name="Stock Price Fetcher",
    metadata={
            "uuid": str(uuid.uuid4()),
            "icon": "https://plus.unsplash.com/premium_photo-1683583961436-fa9efb9f72d7?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8c3RvY2slMjBwcmljZSUyMGljb258ZW58MHx8MHx8fDA%3D",
        }
)
def get_stock_price(stock_handle: str) -> str:
    """Mock: Return fake stock price info."""
    return f"The stock price of {stock_handle} is $420.42 (mocked)."
