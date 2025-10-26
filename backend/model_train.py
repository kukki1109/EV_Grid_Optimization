import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from lightgbm import LGBMRegressor
from backend.preprocess import preprocess_data
import pandas as pd
import numpy as np
import os

MODEL_PATH = "models/model.pkl"

def train_ev_model(csv_path="data/ev_data.csv"):
    # Load dataset
    df = pd.read_csv(csv_path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Preprocess basic features
    df = preprocess_data(df)

    # Ensure battery_capacity column exists
    if 'battery_capacity' not in df.columns:
        df['battery_capacity'] = 50  # default value if missing
        print("Warning: 'battery_capacity' not found. Using default 50 kWh.")

    # Ensure charging_type column exists (categorical 0=Slow, 1=Fast)
    if 'charging_type' in df.columns:
        df['charging_type_num'] = df['charging_type'].apply(lambda x: 1 if str(x).lower() == 'fast' else 0)
    else:
        df['charging_type_num'] = 0  # default slow charger
        print("Warning: 'charging_type' not found. Using default 0 (Slow).")

    # Features and target
    X = df[['hour', 'weekday', 'connectionduration', 'battery_capacity', 'charging_type_num']]
    y = df['charging_power']  # target column

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = LGBMRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Predictions & metrics
    preds = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)

    # Save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model trained successfully! RMSE: {rmse:.3f}, R²: {r2:.3f}")
    return rmse, r2


def predict_energy(hour, weekday, charging_time, battery_capacity=50, charging_type_num=0):
    model = joblib.load(MODEL_PATH)
    X = np.array([[hour, weekday, charging_time, battery_capacity, charging_type_num]])
    prediction = model.predict(X)[0]
    return prediction
