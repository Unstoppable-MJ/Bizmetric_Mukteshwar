# BTCUSD Forecasting Project - Phase 1

This project implements a machine learning pipeline for forecasting BTCUSD returns using ARIMA and Linear Regression.

## Phase 1: Foundation & Data Engineering

### Project Structure
```text
btc_forecasting/
├── data/
│   ├── raw/             # Raw OHLCV data from Binance
│   └── processed/       # Engineered features in Parquet format
├── src/
│   ├── data/            # Data ingestion, validation, and preprocessing
│   ├── features/        # Feature engineering (lags, indicators)
│   └── models/          # Model architectures (placeholders for Phase 2)
├── notebooks/           # Exploratory Data Analysis
├── config.yaml          # Project configuration
└── requirements.txt     # Python dependencies
```

### Setup & Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Data Pipeline
1. **Fetch Data**:
   ```bash
   python src/data/fetch_binance.py
   ```
2. **Validate & Preprocess**:
   ```bash
   python src/data/validate.py
   python src/data/preprocess.py
   ```
3. **Feature Engineering**:
   ```bash
   python src/features/indicators.py
   python src/features/lag_features.py
   ```

The final dataset is saved as `data/processed/btc_features.parquet`.

### Features Detailed
- **Lags**: 1, 2, 3, 6, 12, 24 hours
- **Rolling Stats**: Mean and Standard Deviation (5, 10 hours)
- **Indicators**: RSI, Simple Moving Averages (10, 20 hours)
- **Target**: `next_return` (Log returns for t+1)
