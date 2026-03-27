import pandas as pd
import numpy as np

def generate_sample_data(filename='train_delay_data.csv'):
    """
    Generates a sample dataset for train delay prediction.
    Fields: train_no, current_delay, station_index, next_delay
    """
    np.random.seed(42)
    n_samples = 1000
    
    train_nos = np.random.randint(12000, 13000, n_samples)
    current_delays = np.random.randint(0, 120, n_samples)
    station_indices = np.random.randint(1, 20, n_samples)
    
    # Simple linear relationship + some noise
    # Next delay depends on current delay and station index (as stations progress, delays might increase)
    next_delays = current_delays * 0.9 + station_indices * 2 + np.random.normal(0, 5, n_samples)
    next_delays = np.maximum(0, next_delays)  # Ensure no negative delays
    
    df = pd.DataFrame({
        'train_no': train_nos,
        'current_delay': current_delays,
        'station_index': station_indices,
        'next_delay': next_delays
    })
    
    df.to_csv(filename, index=False)
    print(f"Sample data generated: {filename}")

if __name__ == "__main__":
    generate_sample_data('d:/Project_Intership/Railway_AI_System/ml_model/train_delay_data.csv')
