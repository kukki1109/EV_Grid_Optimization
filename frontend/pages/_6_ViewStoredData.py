import streamlit as st
from pymongo import MongoClient
import pandas as pd

def show():
    st.title("📁 View Stored Predictions")

    MONGO_URI = "mongodb://localhost:27017/ev_database"
    client = MongoClient(MONGO_URI)
    db = client["ev_database"]
    collection = db["predictions"]

    data = list(collection.find({}, {"_id":0}))
    if data:
        df = pd.DataFrame(data)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp", ascending=False)
        st.dataframe(df.head(20))
    else:
        st.info("No predictions stored yet.")
