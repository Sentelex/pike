import langchain_core.tools as lcct
import typing as t
from ..models import icon_process as ip
from ..models import skill as sk

#  Candidate Icon:
#  https://plus.unsplash.com/premium_photo-1683583961436-fa9efb9f72d7?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8c3RvY2slMjBwcmljZSUyMGljb258ZW58MHx8MHx8fDA%3D

class StockPriceSkill(sk.Skill):
    name: str = "Stock Price Fetcher"
    description: str = "Fetch and return current stock price information"
    icon: str = ip.encode_icon_url_safe_utf8("stock-svgrepo-com.svg")

    get_stock_price: t.ClassVar[lcct.StructuredTool]
    @lcct.tool(name.replace(" ", "_"))
    def get_stock_price(stock_handle: str) -> str:
        """
        Mock: Return fake stock price info.
        """
        return f"The stock price of {stock_handle} is $420.42 (mocked)."

    tool: lcct.Tool = get_stock_price
