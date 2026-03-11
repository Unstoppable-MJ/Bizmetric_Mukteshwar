import mlflow
import yaml
import os

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

class ModelLoader:
    """
    Utility to load models from MLflow Model Registry.
    """
    def __init__(self):
        config = load_config()
        mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])

    def load_latest_model(self, model_name: str):
        """
        Loads the latest version of a model, preferring Production over Staging.
        """
        print(f"Loading latest version of {model_name}...")
        
        # Try Production first
        try:
            model_uri = f"models:/{model_name}/Production"
            model = mlflow.sklearn.load_model(model_uri)
            print(f"Loaded {model_name} from Production stage.")
            return model
        except Exception:
            print(f"Production model not found for {model_name}. Fallback to Staging.")
            
        # Try Staging
        try:
            model_uri = f"models:/{model_name}/Staging"
            model = mlflow.sklearn.load_model(model_uri)
            print(f"Loaded {model_name} from Staging stage.")
            return model
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            return None
