import pandas as pd

def preprocess_data(df):
    # Convert timestamp to datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['weekday'] = df['timestamp'].dt.weekday
    else:
        # fallback
        df['hour'] = 0
        df['weekday'] = 0
        print("Warning: 'timestamp' column not found. Default hour and weekday set to 0.")

    # Use charging_time as connection duration
    if 'charging_time' in df.columns:
        df['connectionduration'] = df['charging_time']
    else:
        df['connectionduration'] = 1.0
        print("Warning: 'charging_time' column not found. Using default duration=1.0")

    # Drop missing target values
    if 'charging_power' in df.columns:
        df = df.dropna(subset=['charging_power'])
    else:
        raise ValueError("Target column 'charging_power' not found in dataset.")

    return df
