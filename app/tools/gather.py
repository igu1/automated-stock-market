from app.agents.core import Tool
import json
import requests
import yfinance as yf

class StockPriceTool(Tool):
    name = "stock_price"
    description = "Retrieves the current stock price for a given symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the current price for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            current_price = stock.info.get(
                "regularMarketPrice", stock.info.get("currentPrice")
            )
            return f"{current_price:.4f}" if current_price else f"Could not fetch current price for {symbol}"
        except Exception as e:
            return f"Error fetching current price for {symbol}: {e}"

        
class CompanyInfoTool(Tool):
    name = "company_info"
    description = "Retrieves company information for a given symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the company information for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            company_info_full = yf.Ticker(symbol).info
            if company_info_full is None:
                return f"Could not fetch company info for {symbol}"

            company_info_cleaned = {
                "Name": company_info_full.get("shortName"),
                "Symbol": company_info_full.get("symbol"),
                "Current Stock Price": f"{company_info_full.get('regularMarketPrice', company_info_full.get('currentPrice'))} {company_info_full.get('currency', 'USD')}",
                "Market Cap": f"{company_info_full.get('marketCap', company_info_full.get('enterpriseValue'))} {company_info_full.get('currency', 'USD')}",
                "Sector": company_info_full.get("sector"),
                "Industry": company_info_full.get("industry"),
                "Address": company_info_full.get("address1"),
                "City": company_info_full.get("city"),
                "State": company_info_full.get("state"),
                "Zip": company_info_full.get("zip"),
                "Country": company_info_full.get("country"),
                "EPS": company_info_full.get("trailingEps"),
                "P/E Ratio": company_info_full.get("trailingPE"),
                "52 Week Low": company_info_full.get("fiftyTwoWeekLow"),
                "52 Week High": company_info_full.get("fiftyTwoWeekHigh"),
                "50 Day Average": company_info_full.get("fiftyDayAverage"),
                "200 Day Average": company_info_full.get("twoHundredDayAverage"),
                "Website": company_info_full.get("website"),
                "Summary": company_info_full.get("longBusinessSummary"),
                "Analyst Recommendation": company_info_full.get("recommendationKey"),
                "Number Of Analyst Opinions": company_info_full.get("numberOfAnalystOpinions"),
                "Employees": company_info_full.get("fullTimeEmployees"),
                "Total Cash": company_info_full.get("totalCash"),
                "Free Cash flow": company_info_full.get("freeCashflow"),
                "Operating Cash flow": company_info_full.get("operatingCashflow"),
                "EBITDA": company_info_full.get("ebitda"),
                "Revenue Growth": company_info_full.get("revenueGrowth"),
                "Gross Margins": company_info_full.get("grossMargins"),
                "Ebitda Margins": company_info_full.get("ebitdaMargins"),
            }
            return json.dumps(company_info_cleaned, indent=2)
        except Exception as e:
            return f"Error fetching company profile for {symbol}: {e}"


class HistoricalStockPricesTool(Tool):
    name = "historical_stock_prices"
    description = (
        "Retrieves comprehensive historical stock prices and associated metrics for "
        "different time frames ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', "
        "'10y', 'ytd', 'max') for a given symbol."
    )

    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the historical prices for."
        },
        "time_frame": {
            "type": "string",
            "description": (
                "The time frame to fetch historical data for. Can be ['1d', '5d', '1mo', "
                "'3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']"
            ),
            "default": "1mo",
            "nullable": True
        }
    }

    output_type = "string"

    def forward(self, symbol: str, time_frame: str = "1mo") -> str:
        try:
            stock = yf.Ticker(symbol)
            historical_data = stock.history(period=time_frame)
            data = {
                "Symbol": symbol,
                "Time_Frame": time_frame,
                "Statistics": {},
            }
            if len(historical_data) == 0:
                data["Data"] = []
                data["Statistics"] = {
                    "Message": "No historical data returned for this symbol/time_frame."
                }
                return json.dumps(data, indent=2)
            records = historical_data.reset_index().to_dict(orient="records")

            for row in records:
                if "Date" in row and hasattr(row["Date"], "strftime"):
                    row["Date"] = row["Date"].strftime("%Y-%m-%d")

            data["Data"] = records
            data["Statistics"] = {
                "Start_Date": historical_data.index.min().strftime('%Y-%m-%d'),
                "End_Date": historical_data.index.max().strftime('%Y-%m-%d'),
                "Total_Records": len(historical_data),
                "Highest_Price": float(historical_data['High'].max()),
                "Lowest_Price": float(historical_data['Low'].min()),
                "Average_Close": float(historical_data['Close'].mean()),
                "Volume_Change": float(historical_data['Volume'].pct_change().mean())
                                if len(historical_data) > 1 else None,
            }
            return json.dumps(data, indent=2)

        except Exception as e:
            return f"Error fetching historical stock prices for {symbol}: {e}"


class StockFundamentalsTool(Tool):
    name = "stock_fundamentals"
    description = "Retrieves key fundamentals for a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the fundamentals for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            fundamentals = {
                "symbol": symbol,
                "company_name": info.get("longName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("forwardPE", "N/A"),
                "pb_ratio": info.get("priceToBook", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "eps": info.get("trailingEps", "N/A"),
                "beta": info.get("beta", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
            }
            return json.dumps(fundamentals, indent=2)
        except Exception as e:
            return f"Error getting fundamentals for {symbol}: {e}"


class IncomeStatementTool(Tool):
    name = "income_statement"
    description = "Retrieves the income statement for a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the income statement for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            financials = stock.financials
            return financials.to_json(orient="index")
        except Exception as e:
            return f"Error fetching income statements for {symbol}: {e}"


class KeyFinancialRatiosTool(Tool):
    name = "key_financial_ratios"
    description = "Retrieves key financial ratios for a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the financial ratios for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            key_ratios = stock.info
            return json.dumps(key_ratios, indent=2)
        except Exception as e:
            return f"Error fetching key financial ratios for {symbol}: {e}"


class AnalystRecommendationsTool(Tool):
    name = "analyst_recommendations"
    description = "Retrieves analyst recommendations for a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch analyst recommendations for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            stock = yf.Ticker(symbol)
            recommendations = stock.recommendations
            return recommendations.to_json(orient="index")
        except Exception as e:
            return f"Error fetching analyst recommendations for {symbol}: {e}"


class CompanyNewsTool(Tool):
    name = "company_news"
    description = "Retrieves the latest company news for a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the latest news for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            news = yf.Ticker(symbol).news
            return json.dumps(news[:3], indent=2)
        except Exception as e:
            return f"Error fetching company news for {symbol}: {e}"


class TechnicalIndicatorsTool(Tool):
    name = "technical_indicators"
    description = "Retrieves the technical indicators for the last month of a given stock symbol."
    inputs = {
        "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the technical indicators for."
        }
    }
    output_type = "string"

    def forward(self, symbol: str) -> str:
        try:
            indicators = yf.Ticker(symbol).history(period="1mo")
            return indicators.to_json(orient="index")
        except Exception as e:
            return f"Error fetching technical indicators for {symbol}: {e}"


class TickerByNameTool(Tool):
    name = "ticker_by_name"
    description = "Fetches the stock ticker for a given company name."
    inputs = {
        "company_name": {
            "type": "string",
            "description": "The name of the company to fetch the stock ticker for."
        }
    }
    output_type = "string"

    def forward(self, company_name: str) -> str:
        try:
            search_url = f"https://query1.finance.yahoo.com/v1/finance/search"
            params = {
                "q": company_name,
                "quotesCount": 1,
                "newsCount": 0,
                "fields": "symbol",
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(search_url, params=params, headers=headers)
            data = response.json()
            if "quotes" in data and data["quotes"]:
                return data["quotes"][0]["symbol"]
            else:
                return None
        except Exception as e:
            return f"Error fetching ticker for {company_name}: {e}"
