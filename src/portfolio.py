import pandas as pd

class StockPortfolio:
    def __init__(self):
        self.stocks = {}  # Dictionary to hold stock data

    def add_stock(self, ticker, shares, purchase_price):
        """Add a new stock to the portfolio"""
        self.stocks[ticker] = {"Shares": shares, "Purchase Price": purchase_price}

    def remove_stock(self, ticker):
        """Remove a stock from portfolio"""
        if ticker in self.stocks:
            del self.stocks[ticker]
        else:
            print("Stock not found in portfolio.")

    def display_portfolio(self):
        """Display current portfolio"""
        return pd.DataFrame(self.stocks).T

# Test the Portfolio Class
if __name__ == "__main__":
    portfolio = StockPortfolio()
    portfolio.add_stock("AAPL", 10, 150.00)
    portfolio.add_stock("GOOGL", 5, 2800.00)
    print(portfolio.display_portfolio())
