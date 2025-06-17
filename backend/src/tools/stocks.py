import langchain_core.tools as lcct
from ..models import skill as sk


class StockPriceSkill(sk.Skill):
    name: str = "Stock Price Fetcher"
    description: str = "Fetch and return current stock price information"
    icon: str = "📈"

    def get_stock_price(stock_handle: str) -> str:
        """
        Mock: Return fake stock price info.
        """
        return f"The stock price of {stock_handle} is $420.42 (mocked)."

    tool: lcct.Tool = lcct.tool(name.replace(" ","_"))(get_stock_price)
