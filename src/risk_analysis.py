import numpy as np
import pandas as pd

class RiskAnalysis:
    @staticmethod
    def calculate_daily_returns(stock_data):
        """Calculate daily percentage change"""
        if stock_data.empty:
            return pd.Series(dtype="float64")
        return stock_data['Close'].pct_change().dropna()

    @staticmethod
    def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.02):
        """Compute Sharpe Ratio"""
        if daily_returns.empty:
            return np.nan
        return (daily_returns.mean() - risk_free_rate) / daily_returns.std()
    
    @staticmethod
    def calculate_volatility(daily_returns):
        """Calculate volatility (Standard Deviation)"""
        if daily_returns.empty:
            return np.nan
        return daily_returns.std()
    
    @staticmethod
    def calculate_value_at_risk(daily_returns, confidence_level=0.95):
        """Calculate VaR at given confidence level"""
        if daily_returns.empty:
            return np.nan
        return -np.percentile(daily_returns, (1 - confidence_level) * 100)
    
    @staticmethod
    def compare_with_market(stock_data, market_data):
        """Compare stock performance with S&P 500 using correlation"""
        if stock_data.empty or market_data.empty:
            # return pd.DataFrame({"Stock Returns": [], "S&P 500 Returns": []})
            return None
        stock_returns = RiskAnalysis.calculate_daily_returns(stock_data)
        market_returns = RiskAnalysis.calculate_daily_returns(market_data)
        
        if stock_returns.empty or market_returns.empty:
            # return pd.DataFrame({"Stock Returns": [], "S&P 500 Returns": []})
            return None
        
        comparison_df = pd.DataFrame({"Stock Returns": stock_returns, "S&P 500 Returns": market_returns})
        return comparison_df.corr()  # Correlation between stock and market
    
    @staticmethod
    def calculate_portfolio_correlation(stock_data_dict):
        """Calculate correlation matrix for all stocks in portfolio"""
        daily_returns = {}
        
        for ticker, data in stock_data_dict.items():
            daily_returns[ticker] = RiskAnalysis.calculate_daily_returns(data)

        daily_returns_df = pd.DataFrame(daily_returns).dropna()
        return daily_returns_df.corr()

# Test the Risk Analysis
if __name__ == "__main__":
    # Simulated Stock Price Data
    stock_prices = pd.DataFrame({"Close": [100, 102, 98, 105, 107]})

    # Compute Metrics
    daily_returns = RiskAnalysis.calculate_daily_returns(stock_prices)
    sharpe_ratio = RiskAnalysis.calculate_sharpe_ratio(daily_returns)
    volatility = RiskAnalysis.calculate_volatility(daily_returns)
    var_95 = RiskAnalysis.calculate_value_at_risk(daily_returns)

    # Print Results
    print("Daily Returns:\n", daily_returns)
    print("Sharpe Ratio:", sharpe_ratio)
    print("Volatility:", volatility)
    print("VaR (95%):", var_95)
