from smolagents import Tool
import requests

class StockPricePredictorTool(Tool):
    name = "stock_price_predictor_tool"
    description = "Predict the price of a stock using a dummy API."

    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to predict the price for (e.g., 'AAPL').",
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        """
        Calls a dummy API to predict the price of a stock.

        Args:
            symbol (str): The stock symbol.

        Returns:
            str: A string containing the predicted stock price or an error message.
        """
        dummy_url = f"https://dummyapi.example.com/predict/{symbol}"
        try:
            response = requests.get(dummy_url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            return f"The predicted price for {symbol} is: 1002.50"
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"

if __name__ == '__main__':
    # Example usage
    tool = StockPricePredictorTool()
    symbol = "AAPL"
    result = tool.forward(symbol)
    print(result)