import src.pike_tool as pt
import pydantic as pdc


class GetStockPriceArgs(pdc.BaseModel):
    stock_handle: str = pdc.Field(
        description="Ticker symbol for the stock for which information is requested."
    )


@pt.pike_tool(display="Get Stock Price", 
              icon="stock-svgrepo-com.svg",
              args_schema=GetStockPriceArgs)
def get_stock_price(stock_handle: str) -> str:
    """Mock: Return fake stock price info."""
    return f"The stock price of {stock_handle} is $420.42 (mocked)."
