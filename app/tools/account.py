from smolagents import Tool
from alpaca.trading.client import TradingClient

class AlpacaTradingBaseTool(Tool):
    def __init__(self):
        super().__init__()
        self.trading_client = TradingClient("PKP9BIP2GUWJETFX8EFS", "vGsufC5KafplcjxDwemIK1h9dbgmLyF8WiqLZ6ol", paper=True)

class AccountInfoTool(AlpacaTradingBaseTool,Tool):
    name = "account_info_tool"
    description = "Retrieve account details, including buying power and trading restrictions."

    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        try:
            account = self.trading_client.get_account()
            trading_status = "restricted from trading" if account.trading_blocked else "allowed to trade"
            buying_power = account.buying_power
            return (
                f"Account is {trading_status}.\n"
                f"Buying power available: ${buying_power}."
            )
        except Exception as e:
            return f"An error occurred: {e}"

class PortfolioGainLossTool(AlpacaTradingBaseTool,Tool):
    name = "portfolio_gain_loss_tool"
    description = "Calculate the daily profit or loss of the portfolio."

    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        try:
            account = self.trading_client.get_account()

            balance_change = float(account.equity) - float(account.last_equity)

            return f"Today's portfolio balance change: ${balance_change:.2f}"
        except Exception as e:
            return f"An error occurred: {e}"

