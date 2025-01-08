from smolagents import Tool
from alpaca.trading.client import TradingClient

class AlpacaTradingBaseTool(Tool):
    def __init__(self):
        super().__init__()
        self.trading_client = TradingClient("PKE6BISKQV2W3QTD8K28", "oXhV8HblBc05eBlxfXBV8FZl8RxYqgHjAsH4tlcV", paper=True)

class PortfolioTool(AlpacaTradingBaseTool):
    name = "portfolio_tool"
    description = "Retrieve portfolio details or open positions from Alpaca's trading API."

    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to check the open position for (e.g., 'AAPL'). Leave empty to fetch all positions.",
            "nullable": True,
        }
    }
    output_type = "string"

    def forward(self, symbol: str = None) -> str:
        try:
            if symbol:
                position = self.trading_client.get_open_position(symbol)
                return f"Open position for {symbol}: {position.qty} shares at {position.avg_entry_price} average price."
            else:
                portfolio = self.trading_client.get_all_positions()
                portfolio_summary = [
                    f"{position.qty} shares of {position.symbol} at {position.avg_entry_price} average price."
                    for position in portfolio
                ]
                return "\n".join(portfolio_summary) if portfolio_summary else "No open positions found."

        except Exception as e:
            return f"An error occurred: {e}"