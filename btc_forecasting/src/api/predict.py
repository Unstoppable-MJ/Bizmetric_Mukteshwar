import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models.model_loader import ModelLoader

class Predictor:
    """
    Handles internal prediction logic using the latest registered model.
    """
    def __init__(self, model_name="lr_btc_model"):
        self.loader = ModelLoader()
        self.model = self.loader.load_latest_model(model_name)
        if self.model is None:
            print(f"Warning: Could not load model {model_name}.")

    def predict(self, input_features: dict):
        """
        Runs prediction on a dictionary of features.
        """
        if self.model is None:
            return None
            
        # 1. Special handling for ARIMA (statsmodels)
        if "statsmodels" in str(type(self.model)):
            try:
                # Attempt to update model with latest price
                latest_p = input_features.get('close') or input_features.get('lag_1')
                if latest_p is not None:
                    try:
                        # Attempt update; if it fails due to index gap, we skip it
                        temp_model = self.model.apply([latest_p])
                        forecast = temp_model.forecast(steps=1)
                    except Exception:
                        # Fallback: forecast from original model
                        forecast = self.model.forecast(steps=1)
                else:
                    forecast = self.model.forecast(steps=1)
                
                # Convert forecast to float, handle Series/Array
                if hasattr(forecast, 'iloc'):
                    val = float(forecast.iloc[0])
                else:
                    val = float(forecast[0])

                # Final guard against NaN
                if np.isnan(val):
                    return None
                return val
            except Exception as e:
                print(f"ARIMA Forecast Error: {e}")
                return None

        # 2. Standard handling for Sklearn/Linear Regression
        df_input = pd.DataFrame([input_features])
        prediction = self.model.predict(df_input)
        
        if hasattr(prediction, "__iter__"):
            return float(prediction[0])
        return float(prediction)
