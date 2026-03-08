import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import yaml
import numpy as np
import joblib

# Page configuration
st.set_page_config(page_title="BTCUSD ML Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Premium Look ---
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #30363d;
    }
    h1, h2, h3 {
        color: #58a6ff;
    }
</style>
""", unsafe_allow_html=True)

# --- Load Project Config ---
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()

# --- Helper Functions ---
@st.cache_data
def load_data():
    df = pd.read_parquet(config['data']['processed_path'])
    df['timestamp'] = pd.to_datetime(df.index)
    return df

def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

# --- Sidebar Navigation ---
st.sidebar.title("🚀 BTC Forecast")
selection = st.sidebar.radio("Navigation", 
    ["Market Overview", "Technical Analysis", "Model Performance & Comparison"])

# --- Main Dashboard ---
df = load_data()

if selection == "Market Overview":
    st.title("📊 BTC Price Overview")
    
    # Section 1: Price Overview
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], name='BTC Price', line=dict(color='#f7931a', width=2)))
    fig.update_layout(
        title='BTCUSD Closing Price (1H)',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        template='plotly_dark',
        height=600,
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary Statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${df['close'].iloc[-1]:,.2f}")
    col2.metric("24h Change", f"{((df['close'].iloc[-1] / df['close'].shift(24).iloc[-1]) - 1) * 100:.2f}%")
    col3.metric("RSI", f"{df['RSI'].iloc[-1]:.2f}")
    col4.metric("Volume", f"{df['volume'].iloc[-1]:.2f}")

elif selection == "Technical Analysis":
    st.title("📈 Technical Indicators")
    
    indicator_choice = st.selectbox("Select Indicator", ["RSI & Moving Averages", "MACD"])
    
    if indicator_choice == "RSI & Moving Averages":
        # RSI and Price with MAs
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])
        
        # Price and MAs
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], name='Price', line=dict(color='white', width=1)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['moving_average_10'], name='SMA 10', line=dict(color='#58a6ff', width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['moving_average_20'], name='SMA 20', line=dict(color='#ff7b72', width=1.5)), row=1, col=1)
        
        # RSI
        fig.add_trace(go.Scatter(x=df['timestamp'], y=df['RSI'], name='RSI', line=dict(color='#bc8cff', width=1)), row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
        
        fig.update_layout(template='plotly_dark', height=700, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # MACD calculate
        macd, signal = calculate_macd(df['close'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['timestamp'], y=macd, name='MACD', line=dict(color='#58a6ff')))
        fig.add_trace(go.Scatter(x=df['timestamp'], y=signal, name='Signal', line=dict(color='#ff7b72')))
        fig.update_layout(title="MACD Oscillator", template='plotly_dark', height=500)
        st.plotly_chart(fig, use_container_width=True)

elif selection == "Model Performance & Comparison":
    st.title("🤖 Model Comparison & Forecasts")
    
    # Section 3: Model Predictions Visualization
    st.subheader("Forecast Comparison (Test Set)")
    
    # Handle data splitting (consistent with evaluation)
    split_idx = int(len(df) * config['models']['train_test_split'])
    test_df = df.iloc[split_idx:].copy()
    
    # Load Models & Generate Predictions
    arima_path = "models/arima/arima_model.pkl"
    lr_path = "models/linear_regression/lr_model.pkl"
    
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=test_df['timestamp'], y=test_df['close'], name='Actual Price', line=dict(color='white', width=1.5)))
    
    if os.path.exists(arima_path):
        model_fit = joblib.load(arima_path)
        forecast_prices = model_fit.forecast(steps=len(test_df))
        fig_pred.add_trace(go.Scatter(x=test_df['timestamp'], y=forecast_prices, name='ARIMA Forecast', line=dict(color='#bc8cff', dash='dash')))
        
    if os.path.exists(lr_path):
        lr_model = joblib.load(lr_path)
        # For LR we need return to price conversion for visual
        lr_features = config['models']['linear_regression']['features']
        returns_pred = lr_model.predict(test_df[lr_features])
        
        # Convert cumulative returns back to price
        last_train_price = df['close'].iloc[split_idx-1]
        price_pred = last_train_price * np.exp(np.cumsum(returns_pred))
        fig_pred.add_trace(go.Scatter(x=test_df['timestamp'], y=price_pred, name='Linear Regression Forecast', line=dict(color='#58a6ff', dash='dot')))
        
    fig_pred.update_layout(template='plotly_dark', height=600, yaxis_title="Price (USD)")
    st.plotly_chart(fig_pred, use_container_width=True)
    
    # Section 4 & 5: Performance Metrics
    st.divider()
    st.subheader("Performance Metrics (Model Comparison)")
    
    perf_path = "monitoring/model_performance.json"
    if os.path.exists(perf_path):
        with open(perf_path, "r") as f:
            perf_data = json.load(f)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**ARIMA Metrics**")
            st.json(perf_data.get("arima", {}))
            
        with col2:
            st.write("**Linear Regression Metrics**")
            st.json(perf_data.get("linear_regression", {}))
            
        # Comparison Table/Verdict
        st.markdown("### 🏆 Comparison Verdict")
        metrics_list = []
        for model, metrics in perf_data.items():
            metrics['Model'] = model.upper()
            metrics_list.append(metrics)
        
        metrics_df = pd.DataFrame(metrics_list).set_index('Model')
        st.table(metrics_df)
        
        best_model = metrics_df['RMSE'].idxmin()
        st.success(f"Execution Summary: **{best_model}** is currently the best performing model based on RMSE.")
    else:
        st.warning("Performance metrics report not found. Run evaluation first.")
