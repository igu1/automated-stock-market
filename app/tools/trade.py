from smolagents import Tool
from alpaca.trading.requests import (
    MarketOrderRequest,
    LimitOrderRequest,
    TakeProfitRequest,
    StopLossRequest,
    TrailingStopOrderRequest,
    GetOrdersRequest,
)
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass, QueryOrderStatus
from alpaca.trading.client import TradingClient

class AlpacaTradingBaseTool(Tool):
    def __init__(self):
        super().__init__()
        self.trading_client = TradingClient("PKP9BIP2GUWJETFX8EFS", "vGsufC5KafplcjxDwemIK1h9dbgmLyF8WiqLZ6ol", paper=True)        
class MarketOrderTool(AlpacaTradingBaseTool, Tool):
    name = "market_order_tool"
    description = "Place a market order to buy or sell assets."

    inputs = {
        "symbol": {"type": "string", "description": "The symbol of the asset (e.g., SPY, BTC/USD)."},
        "qty": {"type": "number", "description": "The quantity of the asset to trade."},
        "action": {"type": "string", "description": "'buy' or 'sell'."},
    }
    output_type = "string"

    def forward(self, symbol: str, qty: float, action: str) -> str:
        try:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY if action.lower() == "buy" else OrderSide.SELL,
                time_in_force=TimeInForce.DAY,
            )
            market_order = self.trading_client.submit_order(order_data=market_order_data)
            return f"Market order placed: {market_order}"
        except Exception as e:
            return f"An error occurred: {e}"


class LimitOrderTool(AlpacaTradingBaseTool, Tool):
    name = "limit_order_tool"
    description = "Place a limit order to buy or sell assets."

    inputs = {
        "symbol": {"type": "string", "description": "The symbol of the asset (e.g., SPY, BTC/USD)."},
        "limit_price": {"type": "number", "description": "The limit price for the order."},
        "notional": {"type": "number", "description": "The notional value for the trade."},
        "action": {"type": "string", "description": "'buy' or 'sell'."},
    }
    output_type = "string"

    def forward(self, symbol: str, limit_price: float, notional: float, action: str) -> str:
        try:
            limit_order_data = LimitOrderRequest(
                symbol=symbol,
                limit_price=limit_price,
                notional=notional,
                side=OrderSide.BUY if action.lower() == "buy" else OrderSide.SELL,
                time_in_force=TimeInForce.DAY,
            )
            limit_order = self.trading_client.submit_order(order_data=limit_order_data)
            return f"Limit order placed: {limit_order}"
        except Exception as e:
            return f"An error occurred: {e}"

class ShortOrderTool(AlpacaTradingBaseTool, Tool):
    name = "short_order_tool"
    description = "Place a short order to sell assets you don't own."

    inputs = {
        "symbol": {"type": "string", "description": "The symbol of the asset (e.g., SPY)."},
        "qty": {"type": "number", "description": "The quantity of the asset to short."},
    }
    output_type = "string"

    def forward(self, symbol: str, qty: float) -> str:
        try:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.GTC,
            )
            short_order = self.trading_client.submit_order(order_data=market_order_data)
            return f"Short order placed: {short_order}"
        except Exception as e:
            return f"An error occurred: {e}"


class ClientOrderIDTool(AlpacaTradingBaseTool, Tool):
    name = "client_order_id_tool"
    description = "Place a market order with a client order ID and retrieve it later."

    inputs = {
        "symbol": {"type": "string", "description": "The symbol of the asset (e.g., SPY)."},
        "qty": {"type": "number", "description": "The quantity of the asset to trade."},
        "client_order_id": {"type": "string", "description": "The unique client order ID."},
    }
    output_type = "string"

    def forward(self, symbol: str, qty: float, client_order_id: str) -> str:
        try:
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY,
                client_order_id=client_order_id,
            )
            self.trading_client.submit_order(order_data=market_order_data)
            my_order = self.trading_client.get_order_by_client_id(client_order_id)
            return f"Order retrieved: {my_order}"
        except Exception as e:
            return f"An error occurred: {e}"


class BracketOrderTool(AlpacaTradingBaseTool, Tool):
    name = "bracket_order_tool"
    description = "Place a bracket order with stop loss and take profit."

    inputs = {
        "symbol": {"type": "string", "description": "The symbol of the asset (e.g., SPY)."},
        "qty": {"type": "number", "description": "The quantity of the asset to trade."},
        "take_profit_price": {"type": "number", "description": "The take profit price."},
        "stop_loss_price": {"type": "number", "description": "The stop loss price."},
    }
    output_type = "string"

    def forward(self, symbol: str, qty: float, take_profit_price: float, stop_loss_price: float) -> str:
        try:
            bracket_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY,
                time_in_force=TimeInForce.DAY,
                order_class=OrderClass.BRACKET,
                take_profit=TakeProfitRequest(limit_price=take_profit_price),
                stop_loss=StopLossRequest(stop_price=stop_loss_price),
            )
            bracket_order = self.trading_client.submit_order(order_data=bracket_order_data)
            return f"Bracket order placed: {bracket_order}"
        except Exception as e:
            return f"An error occurred: {e}"


class TrailingStopOrderTool(AlpacaTradingBaseTool, Tool):
    name = "trailing_stop_order_tool"
    description = "Place a trailing stop order."

    inputs = {
        "symbol": {"type": "string", "description": "The symbol of the asset (e.g., SPY)."},
        "qty": {"type": "number", "description": "The quantity of the asset to trade."},
        "trail_percent": {"type": "number", "description": "The trailing stop percentage."},
    }
    output_type = "string"

    def forward(self, symbol: str, qty: float, trail_percent: float) -> str:
        try:
            trailing_stop_data = TrailingStopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.SELL,
                time_in_force=TimeInForce.GTC,
                trail_percent=trail_percent,
            )
            trailing_stop_order = self.trading_client.submit_order(order_data=trailing_stop_data)
            return f"Trailing stop order placed: {trailing_stop_order}"
        except Exception as e:
            return f"An error occurred: {e}"


class RetrieveOrdersTool(AlpacaTradingBaseTool, Tool):
    name = "retrieve_orders_tool"
    description = "Retrieve a list of recent orders."

    inputs = {
        "status": {"type": "string", "description": "The status of the orders to retrieve enum(['closed', 'open', 'cancelled'])."},
        "limit": {"type": "number", "description": "The number of orders to retrieve."},
    }
    output_type = "string"

    def forward(self, status: str, limit: int) -> str:
        try:
            get_orders_data = GetOrdersRequest(
                status=QueryOrderStatus[status.upper()],
                limit=limit,
                nested=True,
            )
            orders = self.trading_client.get_orders(filter=get_orders_data)
            return f"Retrieved orders: {orders}"
        except Exception as e:
            return f"An error occurred: {e}"