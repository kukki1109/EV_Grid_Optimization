import sys
import os

# Add EV_Grid_Optimization root folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
from backend.model_train import train_ev_model

st.title("🧠 Train EV Optimization Model")

st.write("""
This tool trains a LightGBM model to predict EV charging power based on features
like hour of the day, weekday, and connection duration.
""")

if st.button("🚀 Train Model"):
    try:
        rmse, r2 = train_ev_model("data/ev_data.csv")  # CSV path same as Kaggle dataset
        st.success("✅ Model trained successfully!")
        st.write(f"**RMSE:** {rmse:.3f}")
        st.write(f"**R² Score:** {r2:.3f}")
    except Exception as e:
        st.error(f"❌ Error: {e}")
