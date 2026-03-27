import pandas as pd
import pandas_ta as ta
import yaml
import os

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def add_indicators(df):
    print("Calculating technical indicators and rolling features...")
    config = load_config()
    feat_config = config['features']
    
    # RSI
    df['RSI'] = ta.rsi(df['close'], length=feat_config['indicators']['rsi'])
    
    # Moving Averages
    for ma in feat_config['indicators']['ma']:
        df[f'moving_average_{ma}'] = ta.sma(df['close'], length=ma)
    
    # Rolling Features
    for window in feat_config['rolling_windows']:
        df[f'rolling_mean_{window}'] = df['close'].rolling(window=window).mean()
        df[f'rolling_std_{window}'] = df['close'].rolling(window=window).std()
    
    return df

def main():
    config = load_config()
    raw_path = config['data']['raw_path']
    processed_path = config['data']['processed_path']
    
    try:
        df = pd.read_parquet(raw_path)
        df_with_indicators = add_indicators(df)
        df_with_indicators.to_parquet(processed_path, index=False)
        print(f"Technical indicators added and saved to {processed_path}.")
    except FileNotFoundError:
        print(f"Error: Raw data file not found at {raw_path}.")

if __name__ == "__main__":
    main()
