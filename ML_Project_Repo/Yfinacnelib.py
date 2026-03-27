import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("dark_background")

# Download data
df = yf.download("BTC-USD", period="1y", interval="1d")

# Fix MultiIndex columns
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Moving averages
df["MA20"] = df["Close"].rolling(20).mean()
df["MA50"] = df["Close"].rolling(50).mean()

close = df["Close"].squeeze()

# Create figure
fig = plt.figure(figsize=(16,10))

# Price chart
ax1 = plt.subplot2grid((5,1), (0,0), rowspan=3)

ax1.plot(df.index, close, linewidth=2.5, label="BTC Close", color="#00ffcc")
ax1.plot(df.index, df["MA20"], label="MA20", color="#ffcc00")
ax1.plot(df.index, df["MA50"], label="MA50", color="#ff6699")

ax1.fill_between(df.index, close, alpha=0.08, color="#00ffcc")

ax1.set_title("🪙 Bitcoin Price (BTC-USD)", fontsize=20, fontweight="bold")
ax1.set_ylabel("Price (USD)")
ax1.legend()
ax1.grid(alpha=0.2)

# Volume chart
ax2 = plt.subplot2grid((5,1), (3,0), rowspan=2, sharex=ax1)
ax2.bar(df.index, df["Volume"], color="#3399ff", alpha=0.4)
ax2.set_ylabel("Volume")
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.show()