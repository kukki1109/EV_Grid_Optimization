import streamlit as st

# ==============================
# Page configuration
# ==============================
st.set_page_config(
    page_title="⚡ EV Grid Optimization Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Main title and description
# ==============================
st.title("⚡ EV Grid Optimization System")
st.markdown("""
Welcome to the **EV Grid Optimization** 🚘  

This platform allows you to:
- Predict EV charging patterns
- Optimize grid stability
- Visualize energy consumption
""")

# ==============================
# Navigation Guide with icons
# ==============================
st.subheader("📍 Navigation Guide")
st.markdown("""
| Page | Description |
|------|-------------|
| 🏠 **Home** | Overview of your project |
| 🧠 **Train Model** | Train your LightGBM or RandomForest prediction model |
| 🔮 **Predict** | Make single or batch predictions |
| 🎛️ **Customize Predict** | Experiment with different scenarios and compare outcomes |
| 📊 **Explore Data** | Analyze datasets visually with charts and statistics |
""")

# ==============================
# Sidebar reminder
# ==============================
st.info("👉 Use the left sidebar to navigate between pages.")
