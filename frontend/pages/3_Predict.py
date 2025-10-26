import sys
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Add EV_Grid_Optimization root folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

MODEL_PATH = "models/model.pkl"

st.set_page_config(page_title="EV Power Prediction", page_icon="🔋", layout="wide")
st.title("🔋 Advanced EV Charging Power Prediction (Interactive + Time-Series)")

# Check if model exists
if not os.path.exists(MODEL_PATH):
    st.warning("⚠️ Please train the model first before using this page!")
    st.stop()

model = joblib.load(MODEL_PATH)

st.markdown("### Enter EV Charging Details")

# --- User Inputs ---
col1, col2, col3 = st.columns(3)

with col1:
    hour = st.slider("⏰ Hour of Connection (0–23)", 0, 23, 10)
    weekday = st.selectbox("📅 Day of Week",
                           ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    weekday_num = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(weekday)

with col2:
    charging_time = st.slider("🔌 Charging Duration (hrs)", 0.1, 24.0, 2.5)
    battery_capacity = st.slider("🔋 Battery Capacity (kWh)", 20, 150, 60)

with col3:
    charging_type = st.radio("⚙️ Charging Type", ["Slow", "Fast"])
    charging_type_num = 1 if charging_type == "Fast" else 0

# --- Single Prediction ---
if st.button("🔮 Predict Power Demand"):
    X = np.array([[hour, weekday_num, charging_time, battery_capacity, charging_type_num]])
    prediction = model.predict(X)[0]

    # Confidence range ±10%
    lower = prediction * 0.9
    upper = prediction * 1.1

    st.success(f"⚡ **Predicted Charging Power:** {prediction:.2f} kW")
    st.write(f"📈 Confidence Range: {lower:.2f} – {upper:.2f} kW")

    # --- Predicted vs Max Power Plot ---
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Predicted Power"],
        y=[prediction],
        name="Predicted Power (kW)",
        marker_color="royalblue",
        text=[f"{prediction:.2f}"],
        textposition="outside"
    ))
    fig.add_trace(go.Bar(
        x=["Max Possible Power"],
        y=[battery_capacity / charging_time],
        name="Max Possible Power (kW)",
        marker_color="lightgray",
        text=[f"{battery_capacity / charging_time:.2f}"],
        textposition="outside"
    ))
    fig.add_trace(go.Scatter(
        x=["Predicted Power"],
        y=[prediction],
        error_y=dict(
            type='data',
            symmetric=False,
            array=[upper - prediction],
            arrayminus=[prediction - lower],
            thickness=2,
            color='red'
        ),
        mode="markers",
        name="Confidence Range (±10%)",
        marker=dict(color="red", size=8)
    ))
    fig.update_layout(title="🔋 Predicted vs Max Possible Power",
                      yaxis_title="Power (kW)", xaxis_title="Category",
                      barmode="group", template="plotly_white", height=450)
    st.plotly_chart(fig, use_container_width=True)

    # --- Time-Series Simulation ---
    st.markdown("### ⏱ Charging Power Across 24 Hours (Time-Series)")
    hours = np.arange(0, 24)
    ts_power = [model.predict([[h, weekday_num, charging_time, battery_capacity, charging_type_num]])[0]
                for h in hours]

    ts_fig = go.Figure()
    ts_fig.add_trace(go.Scatter(
        x=hours,
        y=ts_power,
        mode='lines+markers',
        name='Predicted Power',
        line=dict(color='mediumseagreen', width=3)
    ))
    ts_fig.update_layout(
        title="📈 Predicted Charging Power Hourly",
        xaxis_title="Hour of Day",
        yaxis_title="Charging Power (kW)",
        template="plotly_white",
        height=400
    )
    st.plotly_chart(ts_fig, use_container_width=True)

# --- Comparison Feature ---
st.markdown("### 🧩 Compare Multiple Scenarios")
num_inputs = st.number_input("How many scenarios to compare?", 2, 5, 2)

data = []
for i in range(num_inputs):
    st.markdown(f"#### Scenario {i+1}")
    c1, c2, c3 = st.columns(3)
    with c1:
        h = st.slider(f"Hour (Scenario {i+1})", 0, 23, 10, key=f"h{i}")
        wd = st.selectbox(f"Weekday (Scenario {i+1})", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], key=f"wd{i}")
        wd_num = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].index(wd)
    with c2:
        dur = st.slider(f"Duration (hrs) {i+1}", 0.1, 24.0, 2.0, key=f"d{i}")
        cap = st.slider(f"Battery (kWh) {i+1}", 20, 150, 60, key=f"cap{i}")
    with c3:
        ctype = st.radio(f"Type {i+1}", ["Slow", "Fast"], key=f"ctype{i}")
        ctype_num = 1 if ctype == "Fast" else 0

    X_i = np.array([[h, wd_num, dur, cap, ctype_num]])
    pred_i = model.predict(X_i)[0]
    data.append({
        "Scenario": f"S{i+1}",
        "Hour": h,
        "Duration": dur,
        "Battery": cap,
        "Type": ctype,
        "Predicted Power (kW)": pred_i
    })

if st.button("📊 Compare Predictions"):
    df_compare = pd.DataFrame(data)
    st.dataframe(df_compare)

    fig2 = go.Figure(data=[
        go.Bar(
            x=df_compare["Scenario"],
            y=df_compare["Predicted Power (kW)"],
            text=[f"{v:.2f}" for v in df_compare["Predicted Power (kW)"]],
            textposition="outside",
            marker_color="mediumseagreen"
        )
    ])
    fig2.update_layout(
        title="🔋 Comparison of Multiple EV Charging Scenarios",
        xaxis_title="Scenario",
        yaxis_title="Predicted Power (kW)",
        template="plotly_white",
        height=450
    )
    st.plotly_chart(fig2, use_container_width=True)
