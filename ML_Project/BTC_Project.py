import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_btc_data():

    ticker_symbol = "BTC-USD"
    btc = yf.Ticker(ticker_symbol)

    # Fetch historical data
    hist = btc.history(period="1200d")

    hist = hist[['Open', 'High', 'Low', 'Close', 'Volume']]

    print(hist.tail())

    # -----------------------------
    # Moving Averages
    # -----------------------------
    hist['MA9'] = hist['Close'].rolling(window=9).mean()
    hist['MA21'] = hist['Close'].rolling(window=21).mean()

    # Trend logic
    hist['uptrend'] = np.where(hist['Close'] > hist['MA21'], 1, 0)
    hist['downtrend'] = np.where(hist['Close'] < hist['MA21'], 1, 0)

    hist['upcross'] = np.where(
        (hist['uptrend'] == 1) & (hist['uptrend'].shift(1) == 0),
        hist['Close'],
        np.nan
    )

    hist['downcross'] = np.where(
        (hist['downtrend'] == 1) & (hist['downtrend'].shift(1) == 0),
        hist['Close'],
        np.nan
    )

    # -----------------------------
    # Backtesting Logic
    # -----------------------------
    total_profit = 0
    start_price = None

    for i in range(len(hist)):

        if not np.isnan(hist['upcross'].iloc[i]):
            start_price = hist['upcross'].iloc[i]
            print(f"🟢 BUY on {hist.index[i]} at {start_price:.2f}")

        elif not np.isnan(hist['downcross'].iloc[i]) and start_price is not None:
            end_price = hist['downcross'].iloc[i]

            profit = end_price - start_price
            total_profit += profit

            print(f"🔴 SELL on {hist.index[i]} at {end_price:.2f}")
            print(f"Profit: {profit:.2f}")
            print(f"Profit %: {(profit/start_price)*100:.2f}%\n")

            start_price = None

    print(f"💰 Total Profit: {total_profit:.2f}")

    # -----------------------------
    # Save dataset
    # -----------------------------
    hist.to_csv("BTC_USD.csv")

    # -----------------------------
    # Plotly Chart
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'],
                             mode='lines', name='Close'))

    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA9'],
                             mode='lines', name='MA9'))

    fig.add_trace(go.Scatter(x=hist.index, y=hist['MA21'],
                             mode='lines', name='MA21'))

    # Buy signals
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['upcross'],
        mode='markers',
        name='BUY',
        marker=dict(symbol='triangle-up', size=12, color='green')
    ))

    # Sell signals
    fig.add_trace(go.Scatter(
        x=hist.index,
        y=hist['downcross'],
        mode='markers',
        name='SELL',
        marker=dict(symbol='triangle-down', size=12, color='red')
    ))

    fig.update_layout(
        title="BTC-USD Moving Average Strategy",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )

    fig.show()


if __name__ == "__main__":
    get_btc_data()