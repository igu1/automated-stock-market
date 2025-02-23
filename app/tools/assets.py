from smolagents import Tool
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

class AlpacaTradingBaseTool(Tool):
    def __init__(self):
        super().__init__()
        self.trading_client = TradingClient("PKP9BIP2GUWJETFX8EFS", "vGsufC5KafplcjxDwemIK1h9dbgmLyF8WiqLZ6ol", paper=True)
# class GetAssetsTool(AlpacaTradingBaseTool, Tool):
#     name = "get_assets_tool"
#     description = "Retrieve a list of assets available on Alpaca."

#     inputs = {
#         "asset_class": {
#             "type": "string",
#             "description": "The asset class to search for (e.g., 'US_EQUITY' or 'CRYPTO', 'NSE' or 'BSE').",
#         }
#     }
#     output_type = "string"

#     def forward(self, asset_class: str) -> str:
#         try:
#             search_params = GetAssetsRequest(asset_class=AssetClass[asset_class.upper()])
#             assets = self.trading_client.get_all_assets(search_params)

#             # Format the response
#             asset_list = [f"{asset.symbol}: {asset.name}" for asset in assets]
#             return "\n".join(asset_list) if asset_list else "No assets found for the specified asset class."

#         except Exception as e:
#             return f"An error occurred: {e}"


class CheckAssetTradabilityTool(AlpacaTradingBaseTool, Tool):
    name = "check_asset_tradability_tool"
    description = "Check if a particular asset is tradable on Alpaca."

    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock or crypto symbol to check (e.g., 'AAPL', 'BTC/USD').",
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            asset = self.trading_client.get_asset(symbol)

            if asset.tradable:
                return f"The asset '{symbol}' is tradable on Alpaca."
            else:
                return f"The asset '{symbol}' is not tradable on Alpaca."

        except Exception as e:
            return f"An error occurred: {e}"