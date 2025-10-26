import sys
import os

# Add EV_Grid_Optimization root folder to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st
import pandas as pd
import os

st.title("📁 Upload Kaggle Dataset")

os.makedirs("data", exist_ok=True)
uploaded_file = st.file_uploader("Upload Kaggle EV Dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.to_csv("data/ev_data.csv", index=False)
    st.success("✅ Dataset uploaded successfully!")
    st.dataframe(df.head())
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

