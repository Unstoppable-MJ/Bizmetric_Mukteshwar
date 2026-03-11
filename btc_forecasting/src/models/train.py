import pandas as pd
import numpy as np
import yaml
import mlflow
import os
import joblib
from arima_model import ARIMAModel
from linear_regression_model import LinearRegressionModel
import sys

# Add src to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from evaluation.metrics import calculate_rmse, calculate_mae, calculate_mape, direction_accuracy

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def train_pipeline():
    config = load_config()
    data_path = config['data']['processed_path']
    target_col = 'next_return'
    
    # MLflow Setup
    mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
    mlflow.set_experiment(config['mlflow']['experiment_name'])

    # Load data
    df = pd.read_parquet(data_path)
    
    # Time-series split
    split_idx = int(len(df) * config['models']['train_test_split'])
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    # 1. ARIMA Model
    with mlflow.start_run(run_name="ARIMA"):
        arima_order = config['models']['arima']['order']
        model = ARIMAModel(p=arima_order[0], d=arima_order[1], q=arima_order[2])
        
        # ARIMA typically trained on prices or returns; user asked for close price TS
        model.train(train_df['close'])
        predictions_price = model.predict(steps=len(test_df))
        
        # Calculate returns from predicted prices for evaluation against 'next_return'
        # next_return = log(p_t+1 / p_t) -> we need the last train price to start
        last_train_price = train_df['close'].iloc[-1]
        all_prices = np.concatenate([[last_train_price], predictions_price.values])
        pred_returns = np.log(all_prices[1:] / all_prices[:-1])

        # Metrics
        y_true = test_df[target_col].values
        metrics = {
            "rmse": calculate_rmse(y_true, pred_returns),
            "mae": calculate_mae(y_true, pred_returns),
            "mape": calculate_mape(y_true, pred_returns),
            "direction_accuracy": direction_accuracy(y_true, pred_returns)
        }
        
        # Log to MLflow
        mlflow.log_param("model_type", "ARIMA")
        mlflow.log_params({"p": arima_order[0], "d": arima_order[1], "q": arima_order[2]})
        mlflow.log_metrics(metrics)
        
        model_save_path = "models/arima/arima_model.pkl"
        model.save_model(model_save_path)
        
        # Log artifact and register model
        mlflow.log_artifact(model_save_path)
        model_name = "arima_btc_model"
        mlflow.sklearn.log_model(model.model_fit, "model", registered_model_name=model_name)
        
        # Transition to Staging
        client = mlflow.tracking.MlflowClient()
        versions = client.get_latest_versions(model_name, stages=["None"])
        if versions:
            latest_version = versions[0].version
            client.transition_model_version_stage(
                name=model_name,
                version=latest_version,
                stage="Staging"
            )
        
        print(f"ARIMA Metrics: {metrics}")

    # 2. Linear Regression Model
    with mlflow.start_run(run_name="LinearRegression"):
        lr_features = config['models']['linear_regression']['features']
        model = LinearRegressionModel()
        
        X_train = train_df[lr_features]
        y_train = train_df[target_col]
        X_test = test_df[lr_features]
        y_test = test_df[target_col]
        
        model.train(X_train, y_train)
        predictions = model.predict(X_test)
        
        # Metrics
        y_true = y_test.values
        metrics = {
            "rmse": calculate_rmse(y_true, predictions),
            "mae": calculate_mae(y_true, predictions),
            "mape": calculate_mape(y_true, predictions),
            "direction_accuracy": direction_accuracy(y_true, predictions)
        }
        
        # Log to MLflow
        mlflow.log_param("model_type", "Linear Regression")
        mlflow.log_param("features", str(lr_features))
        mlflow.log_metrics(metrics)
        
        model_save_path = "models/linear_regression/lr_model.pkl"
        model.save_model(model_save_path)
        
        # Log artifact and register model
        mlflow.log_artifact(model_save_path)
        model_name = "lr_btc_model"
        mlflow.sklearn.log_model(model.model, "model", registered_model_name=model_name)

        # Transition to Staging
        versions = client.get_latest_versions(model_name, stages=["None"])
        if versions:
            latest_version = versions[0].version
            client.transition_model_version_stage(
                name=model_name,
                version=latest_version,
                stage="Staging"
            )
        
        print(f"Linear Regression Metrics: {metrics}")


if __name__ == "__main__":
    train_pipeline()
