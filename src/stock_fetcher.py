import yfinance as yf
import pandas as pd

class StockFetcher:
    def __init__(self, tickers):
        self.tickers = tickers

    def get_stock_data(self, period="1y", interval="1d"):
        """Fetch historical stock data"""
        stock_data = {}
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            stock_data[ticker] = stock.history(period=period, interval=interval)
        return stock_data

# Test the Stock Fetcher
if __name__ == "__main__":
    fetcher = StockFetcher(["AAPL", "GOOGL"])
    data = fetcher.get_stock_data()
    for ticker, df in data.items():
        print(f"\n{ticker} Stock Data:\n", df.head())
