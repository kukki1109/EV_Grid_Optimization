import sys
import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Add root folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

st.set_page_config(page_title="EV Data Exploration", layout="wide")
st.title("📊 EV Charging Data Exploration")

DATA_PATH = "data/ev_data.csv"

# Check if dataset exists
if not os.path.exists(DATA_PATH):
    st.warning("⚠️ Dataset not found! Please check `data/ev_data.csv`")
    st.stop()

df = pd.read_csv(DATA_PATH)

# --- Dataset Summary ---
st.header("📝 Dataset Summary")
st.write(f"Total Records: {len(df)}")
st.write(f"Columns: {list(df.columns)}")
st.write("### Statistical Summary")
st.dataframe(df.describe())

# --- Average Charging Power ---
st.header("⚡ Average Charging Power Analysis")

df['charging_time'] = df['charging_time'].replace(0, 0.1)  # prevent divide by zero
df['avg_power'] = df['power_consumed'] / df['charging_time']

# Avg power by hour
avg_hour = df.groupby(df['timestamp'].str[11:13].astype(int))['avg_power'].mean().reset_index()
fig_hour = px.bar(avg_hour, x='timestamp', y='avg_power', labels={'timestamp':'Hour','avg_power':'Avg Power (kW)'},
                  title="Average Charging Power by Hour", text_auto='.2f')
st.plotly_chart(fig_hour, use_container_width=True)

# Avg power by weekday
df['weekday'] = pd.to_datetime(df['timestamp']).dt.day_name()
avg_weekday = df.groupby('weekday')['avg_power'].mean().reindex(
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]).reset_index()
fig_weekday = px.bar(avg_weekday, x='weekday', y='avg_power', text_auto='.2f', title="Average Charging Power by Weekday")
st.plotly_chart(fig_weekday, use_container_width=True)

# Avg power by station
if 'station_id' in df.columns:
    avg_station = df.groupby('station_id')['avg_power'].mean().reset_index()
    fig_station = px.bar(avg_station, x='station_id', y='avg_power', text_auto='.2f', title="Average Charging Power by Station")
    st.plotly_chart(fig_station, use_container_width=True)

# --- Max/Min Charging Duration & Total Energy Delivered ---
st.header("⏱ Charging Duration & Total Energy Delivered")
st.write(f"Maximum Charging Duration: {df['charging_time'].max():.2f} hrs")
st.write(f"Minimum Charging Duration: {df['charging_time'].min():.2f} hrs")
st.write(f"Total Energy Delivered: {df['power_consumed'].sum():.2f} kWh")

# --- Interactive Histogram of Charging Times ---
st.header("📊 Charging Duration Distribution")
fig_hist = px.histogram(df, x='charging_time', nbins=30, title="Histogram of Charging Times", labels={'charging_time':'Duration (hrs)'})
st.plotly_chart(fig_hist, use_container_width=True)

# --- Heatmap: Weekday vs Hour for Energy Consumption ---
st.header("🌡️ Heatmap: Weekday vs Hour Energy Consumption")
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
heatmap_data = df.pivot_table(index='weekday', columns='hour', values='power_consumed', aggfunc='mean').reindex(
    ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
fig_heat = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='Viridis',
    colorbar=dict(title="Avg Power (kW)")
))
fig_heat.update_layout(title="Average Energy Consumed: Weekday vs Hour", xaxis_title="Hour of Day", yaxis_title="Weekday")
st.plotly_chart(fig_heat, use_container_width=True)
