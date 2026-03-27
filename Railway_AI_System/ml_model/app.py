from flask import Flask, request, jsonify
import joblib
import numpy as np
import tensorflow as tf
from datetime import datetime, timedelta

app = Flask(__name__)

# Load models and scalers
lr_model = joblib.load('d:/Project_Intership/Railway_AI_System/ml_model/lr_model.joblib')
lstm_model = tf.keras.models.load_model('d:/Project_Intership/Railway_AI_System/ml_model/lstm_model.keras')
scaler_x = joblib.load('d:/Project_Intership/Railway_AI_System/ml_model/scaler_x.joblib')
scaler_y = joblib.load('d:/Project_Intership/Railway_AI_System/ml_model/scaler_y.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predicts next station delay and estimated arrival time.
    Input JSON: { "train_no": 12051, "current_delay": 15, "station_index": 5 }
    """
    data = request.get_json()
    
    train_no = data.get('train_no')
    current_delay = data.get('current_delay')
    station_index = data.get('station_index')
    
    if None in [train_no, current_delay, station_index]:
        return jsonify({"error": "Missing input fields"}), 400
    
    # 1. Prediction using Linear Regression (as baseline)
    lr_input = np.array([[train_no, current_delay, station_index]])
    lr_pred = lr_model.predict(lr_input)[0]
    
    # 2. Prediction using LSTM
    lstm_input = scaler_x.transform(lr_input)
    lstm_input = lstm_input.reshape((1, 1, 3))
    lstm_pred_scaled = lstm_model.predict(lstm_input, verbose=0)
    lstm_pred = scaler_y.inverse_transform(lstm_pred_scaled)[0][0]
    
    # Estimated arrival time calculation
    # For simplicity, assume arrival time is now + predicted delay + some base travel time (e.g. 30 mins)
    base_travel_time = 30 
    now = datetime.now()
    estimated_arrival = now + timedelta(minutes=int(lstm_pred) + base_travel_time)
    
    return jsonify({
        "train_no": train_no,
        "predicted_delay_lr": f"{lr_pred:.2f} mins",
        "predicted_delay_lstm": f"{lstm_pred:.2f} mins",
        "estimated_arrival": estimated_arrival.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(port=5000, debug=False)
