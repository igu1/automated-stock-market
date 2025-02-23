import requests
import yfinance as yf

# Proxy & Headers
proxy = {
    "http": "http://54.179.44.51:3128",
    "https": "http://54.179.44.51:3128",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Set up session
session = requests.Session()
session.proxies.update(proxy)
session.headers.update(headers)

# Fetch stock data
stock = yf.Ticker("AAPL", session=session)
data = stock.history(period="1mo")

print(data)