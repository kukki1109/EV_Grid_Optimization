import joblib
import pandas as pd
import os

def predict_energy(data: dict):
    model_path = "models/trained_model.pkl"
    if not os.path.exists(model_path):
        raise FileNotFoundError("Trained model not found. Please train it first.")
    model = joblib.load(model_path)
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return float(prediction)
