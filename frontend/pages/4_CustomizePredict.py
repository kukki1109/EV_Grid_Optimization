import sys
import os
import streamlit as st
import joblib
import numpy as np

# Add backend folder to path (adjust if needed)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Set page config
st.set_page_config(page_title="EV Charging Prediction", page_icon="⚡")

st.title("⚡ Predict EV Charging Power")
st.write("""
Use the controls below to predict EV charging power.  
The model uses hour of the day, weekday, charging duration, EV type, station, and charger type.
""")

# -----------------------------
# User Inputs
# -----------------------------
hour = st.slider("Hour of the day (0-23)", min_value=0, max_value=23, value=12)

weekday_name = st.selectbox("Weekday", 
                            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(weekday_name)

charging_time = st.slider("Charging time (hours)", min_value=0.0, max_value=24.0, value=1.0, step=0.1)

# EV Type / Battery Capacity
ev_options = ["EV Model A (40 kWh)", "EV Model B (60 kWh)", "EV Model C (75 kWh)"]
ev_selection = st.selectbox("Select EV Type / Battery Capacity", options=ev_options)
battery_map = {"EV Model A (40 kWh)": 40, "EV Model B (60 kWh)": 60, "EV Model C (75 kWh)": 75}
battery_capacity = battery_map[ev_selection]

# Station selection
stations = ["Station 1", "Station 2", "Station 3"]  # Replace with dataset unique stations
station = st.selectbox("Select Charging Station", options=stations)

# Charging type
charging_type = st.radio("Charging Type", options=["Fast Charger", "Slow Charger"])
charging_type_num = 1 if charging_type == "Fast Charger" else 0

# -----------------------------
# Predict Button
# -----------------------------
if st.button("Predict Charging Power ⚡"):
    try:
        # Load trained model
        model = joblib.load("models/model.pkl")

        # Prepare input array
        # NOTE: Ensure your trained model has the same features in same order
        X_input = np.array([[hour, weekday, charging_time, battery_capacity, charging_type_num]])

        # Predict
        prediction = model.predict(X_input)[0]

        st.success(f"Predicted Charging Power: **{prediction:.2f} kW**")

    except FileNotFoundError:
        st.error("❌ Model file not found! Please train the model first.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
