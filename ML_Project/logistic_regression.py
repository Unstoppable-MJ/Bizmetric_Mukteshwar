# =========================================
# 1. IMPORT LIBRARIES
# =========================================
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =========================================
# 2. DOWNLOAD DATA
# =========================================
gold = yf.download("GC=F", period="5y")
silver = yf.download("SI=F", period="5y")

# Fix multi-level columns (new yfinance)
gold.columns = gold.columns.droplevel(1)
silver.columns = silver.columns.droplevel(1)

# =========================================
# 3. MERGE CLOSING PRICES
# =========================================
data = pd.DataFrame()

data["Gold"] = gold["Close"]
data["Silver"] = silver["Close"]

data.dropna(inplace=True)

# =========================================
# 4. CORRELATION VALUE
# =========================================
corr_value = data["Gold"].corr(data["Silver"])
print("Gold vs Silver Correlation:", corr_value)

# =========================================
# 5. SCATTER PLOT (RELATIONSHIP)
# =========================================
fig1 = px.scatter(
    data,
    x="Gold",
    y="Silver",
    title=f"Gold vs Silver Correlation (r = {corr_value:.2f})",
    trendline="ols",
    template="plotly_dark"
)
fig1.show()

# =========================================
# 6. NORMALIZED PRICE COMPARISON
# =========================================
normalized = data / data.iloc[0]

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=normalized.index,
    y=normalized["Gold"],
    name="Gold (Normalized)",
    line=dict(color="gold")
))

fig2.add_trace(go.Scatter(
    x=normalized.index,
    y=normalized["Silver"],
    name="Silver (Normalized)",
    line=dict(color="silver")
))

fig2.update_layout(
    title="Gold vs Silver Performance Comparison",
    template="plotly_dark"
)

fig2.show()

# =========================================
# 7. ROLLING CORRELATION (VERY IMPORTANT)
# =========================================
rolling_corr = data["Gold"].rolling(60).corr(data["Silver"])

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=rolling_corr.index,
    y=rolling_corr,
    name="60-Day Rolling Correlation",
    line=dict(color="cyan")
))

fig3.update_layout(
    title="Gold vs Silver Rolling Correlation (Dynamic Relationship)",
    template="plotly_dark",
    yaxis=dict(range=[-1, 1])
)

fig3.show()