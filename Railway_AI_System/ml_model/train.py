import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def train_models():
    # Load data
    df = pd.read_csv('d:/Project_Intership/Railway_AI_System/ml_model/train_delay_data.csv')
    
    X = df[['train_no', 'current_delay', 'station_index']]
    y = df['next_delay']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    
    lr_preds = lr_model.predict(X_test)
    print(f"Linear Regression MAE: {mean_absolute_error(y_test, lr_preds)}")
    
    # Save Linear Regression model
    joblib.dump(lr_model, 'd:/Project_Intership/Railway_AI_System/ml_model/lr_model.joblib')
    
    # 2. LSTM Model
    # Preprocessing for LSTM
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    
    X_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1))
    
    # Reshape for LSTM [samples, time_steps, features]
    X_lstm = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
    
    X_train_lstm, X_test_lstm, y_train_lstm, y_test_lstm = train_test_split(X_lstm, y_scaled, test_size=0.2, random_state=42)
    
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(1, 3)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train_lstm, y_train_lstm, epochs=20, verbose=0)
    
    # Save LSTM model and scalers
    model.save('d:/Project_Intership/Railway_AI_System/ml_model/lstm_model.keras')
    joblib.dump(scaler_x, 'd:/Project_Intership/Railway_AI_System/ml_model/scaler_x.joblib')
    joblib.dump(scaler_y, 'd:/Project_Intership/Railway_AI_System/ml_model/scaler_y.joblib')
    
    print("LSTM Model trained and saved.")

if __name__ == "__main__":
    train_models()
