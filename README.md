# **Stock Market Portfolio Analyzer**
#### A Streamlit-based tool for stock portfolio analysis, performance tracking, and risk assessment.

##  **Overview**
The **Stock Market Portfolio Analyzer** is a Python-based web application that allows users to manage their stock portfolios, fetch real-time stock data, analyze performance, assess risks, and generate reports. 

This project demonstrates:
- **Python OOP principles**: Encapsulation, Inheritance, Polymorphism
- **Data manipulation using Pandas**
- **Mathematical computations using NumPy**
- **API integration** for real-world stock data fetching
- **Cloud deployment** on AWS/GCP to showcase DevOps skills

---

## **Features of the Project**

### **1. Portfolio Management**
- Users can **add, remove, and update** stock holdings.
- **Object-Oriented Programming (OOP)** is used to structure stock data.
- Stocks are stored in a **Pandas DataFrame**, allowing easy calculations.

### **2. Stock Price Fetching (Real-time & Historical)**
- **Yahoo Finance API** is used to fetch **real-time** and **historical stock prices**.
- Users can fetch stock data and store historical trends for future analysis.

### **3. Performance Analysis**
- Compute **daily returns, volatility, and Sharpe ratio** using **NumPy**.
- Compare portfolio performance **against the S&P 500 index**.
- Use **Matplotlib and Seaborn** to generate **stock price trend visualizations**.

### **4. Risk Analysis**
- **Value at Risk (VaR)** calculation to measure potential losses.
- **Correlation matrix** between stocks to understand diversification.

### **5. Report Generation**
- Export portfolio insights into **CSV, Excel, or PDF** formats.
- Generate a **PDF report** summarizing portfolio performance, risk metrics, and sector diversification.

### **6. Streamlit Web Dashboard**
- **Interactive UI** to manage the portfolio and visualize stock trends.
- Fetch real-time stock data and analyze performance **directly in the browser**.

---

## **Project Structure**
```
Stock-Market-Analyzer/
│── src/
│   ├── portfolio.py           # Portfolio management (Add/Remove/Update Stocks)
│   ├── stock_fetcher.py       # Fetch stock prices from Yahoo Finance API
│   ├── risk_analysis.py       # Compute risk metrics (VaR, correlation, Sharpe ratio)
│   ├── visualization.py       # Generate plots using Matplotlib & Seaborn
│── app.py                     # Main Streamlit web app
│── requirements.txt           # Python dependencies
│── README.md                  # Project documentation
│── .gitignore                 # Ignore virtual env and secrets
│── .streamlit/                 # Streamlit configuration
```

---

## **Installation Guide**

### **1. Clone the Repository**
```bash
git clone git@github.com:Pratham-mehta/Stock-Market-Analyzer.git
cd Stock-Market-Analyzer
```

### **2. Create a Virtual Environment & Activate**
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Usage Instructions**
### **Run the Streamlit Web App**
```bash
streamlit run app.py
```
- This will open a web browser with the **Stock Market Portfolio Analyzer** interface.

### **Using the Web App**
1. **Add Stocks to Portfolio**:
   - Enter stock tickers (e.g., `AAPL,GOOGL`).
   - Specify number of shares & purchase price.
   - Click **"Add to Portfolio"**.

2. **Fetch Stock Data**:
   - Click **"Fetch Data"** to retrieve real-time/historical stock prices.

3. **Analyze Performance**:
   - Select a stock and click **"Analyze Performance"** to compute returns, volatility, and Sharpe ratio.

4. **Portfolio Risk Analysis**:
   - Click **"Analyze Portfolio Risk"** to compute **VaR, correlation matrix, and sector diversification**.

5. **Generate Reports**:
   - Export portfolio summary as **CSV, Excel, or PDF**.

---

## **Example Visualizations**
The tool provides **data-driven insights** through graphs:
1. **Stock Price Trend**
   - View historical closing prices of stocks.
2. **Portfolio Correlation Matrix**
   - Understand **diversification & risk exposure**.
3. **Sector Diversification Pie Chart**
   - Visualize sector allocations in the portfolio.

---

## **Known Issues & Fixes**
- **PDF Export Fails?**  
  - Install `wkhtmltopdf` manually:
    ```bash
    brew install wkhtmltopdf  # macOS
    sudo apt-get install wkhtmltopdf  # Linux
    ```
  - Ensure `pdfkit` is properly configured in `app.py`:
    ```python
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
    ```

- **GitHub Permission Issues?**  
  - Run:
    ```bash
    ssh -T git@github.com
    ```
  - If it fails, regenerate SSH keys and add them to GitHub.

---


## **Contributing**
Want to improve this project? Follow these steps:
1. **Fork the repo** 
2. Create a **new branch** (`git checkout -b feature-new`)
3. Make changes & **commit** (`git commit -m "Added XYZ feature"`)
4. **Push to GitHub** (`git push origin feature-new`)
5. Open a **Pull Request (PR)** 

---

## **License**
This project is licensed under the **MIT License**.

---

## **Contact**
For queries or suggestions, feel free to reach out:
- **GitHub:** [@Pratham-mehta](https://github.com/Pratham-mehta)
- **Email:** pm3483@nyu.edu

---