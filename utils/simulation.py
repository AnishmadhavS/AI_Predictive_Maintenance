import pandas as pd
import streamlit as st

def get_smooth_data(data, key="global"):

    required_cols = ["Temperature", "Pressure", "Vibration", "Current"]
    data = data[required_cols].copy()

    for col in required_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    data = data.dropna().reset_index(drop=True)

    if len(data) < 2:
        st.error("Not enough valid sensor data")
        st.stop()

    if f"{key}_index" not in st.session_state:
        st.session_state[f"{key}_index"] = min(10, len(data)-2)

    if f"{key}_step" not in st.session_state:
        st.session_state[f"{key}_step"] = 0

    steps = 10  # smoothness

    if st.session_state[f"{key}_index"] >= len(data)-1:
        st.session_state[f"{key}_index"] = min(10, len(data)-2)

    idx = st.session_state[f"{key}_index"]
    step = st.session_state[f"{key}_step"]

    row1 = data.iloc[idx]
    row2 = data.iloc[idx+1]

    alpha = step / steps
    current_point = row1 + (row2 - row1) * alpha

    start = max(0, idx-50)
    recent_data = data.iloc[start:idx].copy()

    recent_data = pd.concat(
        [recent_data, pd.DataFrame([current_point])],
        ignore_index=True
    )

    latest = current_point

    st.session_state[f"{key}_step"] += 1

    if st.session_state[f"{key}_step"] >= steps:
        st.session_state[f"{key}_step"] = 0
        st.session_state[f"{key}_index"] += 1

    return recent_data, latest