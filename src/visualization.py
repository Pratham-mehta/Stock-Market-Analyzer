import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

class Visualization:
    @staticmethod
    def plot_stock_prices(stock_data, ticker):
        """Plot Stock Price Trend"""
        fig, ax = plt.subplots(figsize=(10, 5))
        stock_data[ticker]['Close'].plot(ax=ax, title=f"{ticker} Stock Price")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.grid()

        # Use Streamlit to display the figure
        st.pyplot(fig)

    @staticmethod
    def plot_correlation_matrix(stock_data):
        """Plot Correlation Matrix of Stocks"""
        returns = stock_data.pct_change().dropna()
        fig, ax = plt.subplots()
        sns.heatmap(returns.corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Stock Correlation Matrix")
        
        # Use Streamlit to display the figure
        st.pyplot(fig)
