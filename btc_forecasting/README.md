# 🚀 BTC Forecasting Pipeline & ML Dashboard

A full-stack MLOps project for real-time Bitcoin (BTC/USDT) return forecasting. This system integrates automated data ingestion, feature engineering, model training with MLflow tracking, and a dynamic monitoring dashboard.

---

## 📊 Dashboard Preview
*(Insert your dashboard screenshots here to showcase the Prediction Trend, System Logs, and Model Performance)*

> [!TIP]
> **[ PLACEHOLDER: MAIN_DASHBOARD_SCREENSHOT ]**
> *Recommended: An overview of the Prediction Trend chart and Latest Predictions.*

---

## ✨ Key Features
- **Live Data Ingestion**: Automated fetching of OHLCV data from Binance using CCXT.
- **Dual Model Approach**:
    - **ARIMA**: Time-series analysis for trend-based forecasting.
    - **Linear Regression**: Feature-based model using technical indicators and lags.
- **Real-Time Inference**: FastAPI-powered pipeline generating hourly return forecasts.
- **Experiment Tracking**: Full integration with **MLflow** for logging parameters, metrics (RMSE, MAE, Directional Accuracy), and model versioning.
- **Monitoring & Drift**: Dynamic dashboard showing **Population Stability Index (PSI)** and KS-tests to detect data drift between training and serving data.
- **Modern UI**: Dark-themed dashboard built with Django, Tailwind CSS, and Chart.js.

---

## 🏗️ Project Structure
```text
btc_forecasting/
├── ML_Dashboard/        # Django-based monitoring dashboard
├── data/
│   ├── raw/             # Raw market data (Parquet)
│   └── processed/       # Engineered features (Parquet)
├── logs/                # Inference and prediction logs
├── mlruns/              # MLflow experiment tracking storage
├── src/
│   ├── api/             # FastAPI inference services & scheduler
│   ├── data/            # Data ingestion & automated refresh scripts
│   ├── features/        # Technical indicators (RSI, MA) & lag features
│   ├── models/          # Model training and loading logic
│   └── monitoring/      # Data drift and PSI calculation engines
├── config.yaml          # Centralized project configuration
└── requirements.txt     # Dependency list
```

---

## 🚀 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configure Tracking
Update `config.yaml` with your local absolute path for MLflow:
```yaml
mlflow:
  tracking_uri: file:///your/absolute/path/btc_forecasting/mlruns
```

### 3. Run the Services
**Start the Inference API (FastAPI):**
```bash
uvicorn src.api.app:app --port 8000
```

**Start the Monitoring Dashboard (Django):**
```bash
cd ML_Dashboard
python manage.py runserver 8005
```

---

## 📈 Evaluation Metrics
The system predicts **log returns** for the next hour. Performance is measured using:
- **Directional Accuracy**: The "Hit Rate" - percentage of times the model correctly predicted the price direction (Up/Down).
- **RMSE/MAE**: Measures the magnitude of prediction error in return units.

---

## 🛡️ Model Health (Drift Detection)
We use **PSI (Population Stability Index)** to compare the distribution of live inference data against the training baseline.
- **PSI < 0.1**: Healthy (Stable)
- **0.1 < PSI < 0.2**: Degraded (Monitor closely)
- **PSI > 0.2**: Drift Detected (Retraining required)

---

## 📸 More Screenshots
> [!NOTE]
> **[ PLACEHOLDER: PERFORMANCE_COMPARISON_SCREENSHOT ]**
> *Showcase the head-to-head ARIMA vs Linear Regression metrics here.*

> [!NOTE]
> **[ PLACEHOLDER: MLFLOW_RUNS_SCREENSHOT ]**
> *Showcase the training history table populated from MLflow data.*

---

## 🛠️ Created By
**Antigravity Assistant** & **USER**
对比分析
