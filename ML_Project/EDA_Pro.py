# ==============================
# ADANI GROUP STOCK ANALYSIS
# ==============================

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 1. Adani Group Stock Tickers
# ------------------------------

adani_stocks = {
    "Adani Enterprises": "ADANIENT.NS",
    "Adani Ports": "ADANIPORTS.NS",
    "Adani Power": "ADANIPOWER.NS",
    "Adani Green Energy": "ADANIGREEN.NS",
    "Adani Total Gas": "ADANITOTAL.NS",
    "Adani Energy Solutions": "ADANIENSOL.NS",
    "Adani Transmission": "ADANITRANS.NS",
    "Ambuja Cements": "AMBUJACEM.NS",
    "ACC": "ACC.NS",
    "AWL Agri Business": "AWL.NS",
    "NDTV": "NDTV.NS"
}

# ------------------------------
# 2. Download Stock Data
# ------------------------------

start_date = "2023-01-01"
end_date = "2026-01-01"

all_data = {}

for company, ticker in adani_stocks.items():
    print(f"Downloading {company}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    all_data[company] = data

print("\n✅ All stock data downloaded!")

# ------------------------------
# 3. Combine Closing Prices
# ------------------------------

close_prices = pd.DataFrame()

for company in all_data:
    close_prices[company] = all_data[company]['Close']

print("\nClosing Price Data:")
print(close_prices.head())

# ------------------------------
# 4. Daily Returns Calculation
# ------------------------------

daily_returns = close_prices.pct_change()

print("\nDaily Returns:")
print(daily_returns.head())

# ------------------------------
# 5. Moving Average Analysis
# ------------------------------

moving_avg_20 = close_prices.rolling(window=20).mean()
moving_avg_50 = close_prices.rolling(window=50).mean()

# ------------------------------
# 6. Plot Stock Prices
# ------------------------------

plt.figure(figsize=(12,6))
close_prices.plot()
plt.title("Adani Group Stock Prices")
plt.xlabel("Date")
plt.ylabel("Price")
plt.show()

# ------------------------------
# 7. Plot Returns Volatility
# ------------------------------

plt.figure(figsize=(12,6))
daily_returns.std().sort_values().plot(kind='bar')
plt.title("Stock Volatility (Risk Comparison)")
plt.ylabel("Standard Deviation")
plt.show()

# ------------------------------
# 8. Example Detailed Analysis
#    (Adani Enterprises)
# ------------------------------

stock_name = "Adani Enterprises"

plt.figure(figsize=(12,6))
plt.plot(close_prices[stock_name], label="Close Price")
plt.plot(moving_avg_20[stock_name], label="20 Day MA")
plt.plot(moving_avg_50[stock_name], label="50 Day MA")

plt.title(f"{stock_name} Moving Average Analysis")
plt.legend()
plt.show()

# ------------------------------
# 9. Performance Summary
# ------------------------------

summary = pd.DataFrame()

summary["Average Return"] = daily_returns.mean()
summary["Risk (Volatility)"] = daily_returns.std()
summary["Total Return %"] = (
    (close_prices.iloc[-1] - close_prices.iloc[0])
    / close_prices.iloc[0]
) * 100

print("\n📊 Performance Summary:")
print(summary.sort_values(by="Total Return %", ascending=False))