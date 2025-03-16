import streamlit as st
from src.portfolio import StockPortfolio
from src.stock_fetcher import StockFetcher
from src.visualization import Visualization
from src.risk_analysis import RiskAnalysis
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import pdfkit
import xlsxwriter
import time

# ✅ Initialize portfolio in session state to persist across button clicks
if "portfolio" not in st.session_state:
    st.session_state.portfolio = StockPortfolio()

# ✅ Store stock data in session state to prevent data loss after each button click
if "stock_data" not in st.session_state:
    st.session_state.stock_data = {}

st.title("📈 Stock Market Portfolio Analyzer")

# ✅ User Input for Stock Portfolio Management
tickers = st.text_input("Enter Stock Tickers (comma-separated)", "AAPL,GOOGL")
shares = st.number_input("Enter number of shares", min_value=1, value=10)
purchase_price = st.number_input("Enter purchase price per share", min_value=1.0, value=100.0)

# ✅ Button to Add Stocks to Portfolio
if st.button("Add to Portfolio", key="add_portfolio"):
    for ticker in tickers.split(","):
        # st.session_state.portfolio.add_stock(ticker.strip(), shares, purchase_price)
        ticker = ticker.strip()
        if ticker in st.session_state.portfolio.stocks:
            st.warning(f"{ticker} is already in your portfolio. Update shares instead.")
        else:
            st.session_state.portfolio.add_stock(ticker, shares, purchase_price)
    st.success(f"Added {tickers} to portfolio!")

# ✅ Fetch Stock Data & Store in Session State
if st.button("Fetch Data", key="fetch_data"):
    fetcher = StockFetcher(tickers.split(","))
    # st.session_state.stock_data = fetcher.get_stock_data()  # Store stock data persistently
    new_stock_data = fetcher.get_stock_data()
    st.session_state.stock_data.update(new_stock_data)  # ✅ Preserve old data instead of overwriting

    # for ticker in tickers.split(","):
    #     Visualization.plot_stock_prices(st.session_state.stock_data, ticker.strip())
    if st.session_state.stock_data:
        for ticker in tickers.split(","):
            if ticker.strip() in st.session_state.stock_data:
                Visualization.plot_stock_prices(st.session_state.stock_data, ticker.strip())
            else:
                st.warning(f"⚠️ No data found for {ticker.strip()}")

# ✅ Display Portfolio Table
st.write("### Your Portfolio:")
portfolio_df = st.session_state.portfolio.display_portfolio()

# ✅ Handle Empty Portfolio Case
if portfolio_df.empty:
    st.write("Portfolio is empty.")
else:
    st.write(portfolio_df)

# ✅ Performance Analysis Section
st.write("## 📊 Performance Analysis")

# Select stock for analysis
selected_ticker = st.selectbox("Select a stock for analysis", tickers.split(","))

# ✅ Button to Analyze Stock Performance
if st.button("Analyze Performance", key="analyze_performance"):
    if selected_ticker not in st.session_state.stock_data:
        st.error("⚠️ Please fetch stock data first using 'Fetch Data'.")
    else:
        stock_data = st.session_state.stock_data[selected_ticker]

        # ✅ Fetch S&P 500 data for correlation analysis
        sp500_data = yf.Ticker("^GSPC").history(period="1y", interval="1d")

        # ✅ Compute Key Performance Metrics
        daily_returns = RiskAnalysis.calculate_daily_returns(stock_data)
        sharpe_ratio = RiskAnalysis.calculate_sharpe_ratio(daily_returns)
        volatility = RiskAnalysis.calculate_volatility(daily_returns)
        correlation_with_market = RiskAnalysis.compare_with_market(stock_data, sp500_data)

        # ✅ Display Performance Metrics
        st.write(f"### 📈 {selected_ticker} Performance Metrics")
        st.write(f"🔹 **Sharpe Ratio:** {sharpe_ratio:.2f}")
        st.write(f"🔹 **Volatility:** {volatility:.4f}")

        if correlation_with_market is not None:
            st.write("🔹 **Stock vs. S&P 500 Correlation:**")
            st.write(correlation_with_market)
        else:
            st.write("⚠️ Correlation data not available.")

# ✅ Risk Analysis Section
st.write("## 🔥 Risk Analysis")

# ✅ Button to Analyze Portfolio Risk
if st.button("Analyze Portfolio Risk", key="analyze_risk"):
    if not st.session_state.stock_data:
        st.error("⚠️ Please fetch stock data first using 'Fetch Data'.")
    else:
        stock_data_dict = st.session_state.stock_data

        # ✅ Compute Portfolio Correlation Matrix
        portfolio_correlation = RiskAnalysis.calculate_portfolio_correlation(stock_data_dict)

        # ✅ Compute Portfolio Value at Risk (VaR)
        portfolio_var = {}
        for ticker, data in stock_data_dict.items():
            daily_returns = RiskAnalysis.calculate_daily_returns(data)
            portfolio_var[ticker] = RiskAnalysis.calculate_value_at_risk(daily_returns)

        # ✅ Display Correlation Matrix
        st.write("### 📌 Portfolio Correlation Matrix")
        st.write(portfolio_correlation)

        # ✅ Display Value at Risk (VaR)
        st.write("### ⚠️ Value at Risk (VaR)")
        var_df = pd.DataFrame.from_dict(portfolio_var, orient='index', columns=["VaR (95%)"])
        st.write(var_df)

        # ✅ Value at Risk (VaR) Bar Chart
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(var_df.index, var_df["VaR (95%)"], color="red")
        ax.set_ylabel("VaR (95%)")
        ax.set_title("Stock Value at Risk (VaR 95%)")
        st.pyplot(fig)

        # ✅ Fetch Sector Information for Sector Diversification
        sectors = {}
        for ticker in tickers.split(","):
            try:
                stock_info = yf.Ticker(ticker.strip()).info
                sectors[ticker.strip()] = stock_info.get("sector", "Unknown")
                time.sleep(1) # Added delay to prevent API blocking
            except:
                sectors[ticker.strip()] = "Unknown"

        # Convert to DataFrame
        sector_df = pd.DataFrame(list(sectors.items()), columns=["Stock", "Sector"])

        # Aggregate by sector
        sector_counts = sector_df["Sector"].value_counts()

        # ✅ Sector Diversification Pie Chart
        st.write("### 🏢 Sector Diversification")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(sector_counts, labels=sector_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title("Portfolio Sector Allocation")
        st.pyplot(fig)
        # fig.savefig("sector_chart.png")

        # ✅ Portfolio Expected Return & Sharpe Ratio
        portfolio_returns = []
        portfolio_weights = []
        total_value = sum([shares * purchase_price for ticker in tickers.split(",")])

        for ticker in tickers.split(","):
            stock_data = yf.Ticker(ticker.strip()).history(period="1y", interval="1d")
            daily_returns = RiskAnalysis.calculate_daily_returns(stock_data)

            # Compute weight of stock in portfolio
            stock_value = shares * purchase_price
            weight = stock_value / total_value
            portfolio_weights.append(weight)

            # Compute mean return
            mean_return = daily_returns.mean()
            portfolio_returns.append(mean_return * weight)  # Weighted Return

        # Compute Portfolio Sharpe Ratio
        portfolio_return = sum(portfolio_returns)
        portfolio_volatility = np.std(portfolio_returns)
        portfolio_sharpe_ratio = (portfolio_return - 0.02) / portfolio_volatility if portfolio_volatility != 0 else 0

        # ✅ Display Portfolio Performance
        st.write("### 📈 Portfolio Performance")
        st.write(f"🔹 **Expected Portfolio Return:** {portfolio_return:.2%}")
        st.write(f"🔹 **Portfolio Sharpe Ratio:** {portfolio_sharpe_ratio:.2f}")

# ✅ Add Export Feature
st.write("## 📤 Export Portfolio Data")

export_format = st.radio("Select export format", ["CSV", "Excel", "PDF"])

if st.button("Download", key="download_data"):
    if portfolio_df.empty:
        st.error("⚠️ Portfolio is empty. Please add stocks first.")
    else:
        if export_format == "CSV":
            csv = portfolio_df.to_csv(index=True)
            st.download_button(label="📥 Download CSV", data=csv, file_name="portfolio_data.csv", mime="text/csv")

        elif export_format == "Excel":
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                portfolio_df.to_excel(writer, sheet_name="Portfolio")
                writer.close()
            st.download_button(label="📥 Download Excel", data=excel_buffer, file_name="portfolio_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        elif export_format == "PDF":
            try:
                # ✅ Fix: Ensure `wkhtmltopdf` is configured correctly
                config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

                # ✅ Compute Total Portfolio Value
                total_value = (portfolio_df["Shares"] * portfolio_df["Purchase Price"]).sum()

                # ✅ Compute Portfolio Expected Return & Sharpe Ratio (Ensure they are available)
                portfolio_returns = []
                portfolio_weights = []
                
                for ticker in portfolio_df.index:
                    stock_data = st.session_state.stock_data.get(ticker, pd.DataFrame())
                    if stock_data.empty:
                        continue
                    
                    daily_returns = RiskAnalysis.calculate_daily_returns(stock_data)
                    
                    # Compute weight of stock in portfolio
                    stock_value = portfolio_df.loc[ticker, "Shares"] * portfolio_df.loc[ticker, "Purchase Price"]
                    weight = stock_value / total_value
                    portfolio_weights.append(weight)
                    
                    # Compute mean return
                    mean_return = daily_returns.mean()
                    portfolio_returns.append(mean_return * weight)  # Weighted Return
                
                # Compute Portfolio Sharpe Ratio
                portfolio_return = sum(portfolio_returns) if portfolio_returns else 0
                portfolio_volatility = np.std(portfolio_returns) if portfolio_returns else 0
                portfolio_sharpe_ratio = (portfolio_return - 0.02) / portfolio_volatility if portfolio_volatility != 0 else 0

                # ✅ Compute Portfolio Value at Risk (VaR)
                portfolio_var = {}
                for ticker in portfolio_df.index:
                    stock_data = st.session_state.stock_data.get(ticker, pd.DataFrame())
                    if stock_data.empty:
                        continue
                    
                    daily_returns = RiskAnalysis.calculate_daily_returns(stock_data)
                    portfolio_var[ticker] = RiskAnalysis.calculate_value_at_risk(daily_returns)

                var_df = pd.DataFrame.from_dict(portfolio_var, orient='index', columns=["VaR (95%)"])

                # ✅ HTML Template for the PDF
                html_template = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 20px;
                            padding: 10px;
                        }}
                        h1 {{
                            text-align: center;
                            color: #333;
                        }}
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 8px;
                            text-align: center;
                        }}
                        th {{
                            background-color: #4CAF50;
                            color: white;
                        }}
                        .summary {{
                            margin-bottom: 20px;
                        }}
                        .metrics {{
                            font-size: 16px;
                        }}
                    </style>
                </head>
                <body>
                    <h1>📈 Stock Market Portfolio Report</h1>
                    
                    <div class="summary">
                        <h2>📌 Portfolio Summary</h2>
                        <p><strong>Total Stocks:</strong> {len(portfolio_df)}</p>
                        <p><strong>Total Portfolio Value:</strong> ${total_value:.2f}</p>
                    </div>

                    <h2>📊 Portfolio Table</h2>
                    {portfolio_df.to_html(index=True)}

                    <h2>🔥 Portfolio Risk Metrics</h2>
                    <p class="metrics"><strong>Expected Return:</strong> {portfolio_return:.2%}</p>
                    <p class="metrics"><strong>Sharpe Ratio:</strong> {portfolio_sharpe_ratio:.2f}</p>

                    <h2>⚠️ Value at Risk (VaR)</h2>
                    {var_df.to_html(index=True)}

                    <h2>🏢 Sector Diversification</h2>
                    <img src="sector_chart.png" alt="Sector Chart" width="80%">
                </body>
                </html>
                """

                # ✅ Generate PDF
                pdf = pdfkit.from_string(html_template, False, configuration=config)

                # ✅ Fix: Properly pass PDF data for download
                st.download_button(label="📥 Download PDF", data=pdf, file_name="portfolio_report.pdf", mime="application/pdf")

            except Exception as e:
                st.error(f"⚠️ PDF export failed. Ensure `wkhtmltopdf` is installed. Error: {str(e)}")
