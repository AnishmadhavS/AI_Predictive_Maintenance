import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
from streamlit_autorefresh import st_autorefresh
from utils.simulation import get_smooth_data

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide")

# ---------- HEADER ----------
st.markdown("""
<div style="font-size:18px;font-weight:600;padding:10px;
background:#1f1f2e;border-radius:8px;margin-bottom:10px;">
AI Predictions
</div>
""", unsafe_allow_html=True)

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=2000, key="ai_refresh")

# ---------- LOAD DATA ----------
data = pd.read_csv(os.path.join('data', 'sensor_data.csv'))

# ---------- SMOOTH SIMULATION ----------
recent_data, latest = get_smooth_data(data, key="ai")

# ---------- SENSOR VALUES ----------
temp = latest['Temperature']
pressure = latest['Pressure']
vibration = latest['Vibration']
flow = latest['Current']

# ---------- AI CALCULATIONS ----------
fp = (temp/250)*0.4 + (pressure/200)*0.3 + (vibration/2)*0.2 + (flow/100)*0.1
rul = int((1-fp)*100)
anomaly = vibration*0.5 + temp*0.3
future = temp + np.random.uniform(-5,10)

# ---------- COLOR LOGIC ----------
def color(val, low, mid, reverse=False):
    if reverse:
        if val <= mid: return "red"
        elif val <= low: return "yellow"
        else: return "green"
    else:
        if val <= low: return "green"
        elif val <= mid: return "yellow"
        else: return "red"

# ---------- GRAPH FUNCTION ----------
def g(series, color_val, title, y_label):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=series,
        mode='lines',
        line=dict(color=color_val, width=3)
    ))

    fig.update_layout(
        height=200,
        title=title,
        template="plotly_dark",

        # ✅ AXIS LABELS
        xaxis_title="Time",
        yaxis_title=y_label,

        # ✅ REDUCE FLICKER
        yaxis=dict(
            range=[
                float(min(series)) * 0.95,
                float(max(series)) * 1.05
            ]
        ),

        margin=dict(l=10, r=10, t=30, b=10)
    )

    return fig

# ---------- SERIES ----------
fp_series = np.linspace(0.1, fp, 50)
rul_series = np.linspace(rul, 0, 50)
an_series = np.linspace(20, anomaly, 50)
lstm_series = np.linspace(temp, future, 50)

# =====================================================
# 🔵 AI GRAPHS (2x2)
# =====================================================
c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        g(fp_series, color(fp,0.4,0.7),
          "Failure Probability",
          "Probability (0 - 1)"),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        g(rul_series, color(rul,60,30,True),
          "Remaining Useful Life",
          "Days"),
        use_container_width=True
    )

c3, c4 = st.columns(2)

with c3:
    st.plotly_chart(
        g(an_series, color(anomaly,80,100),
          "Anomaly Score",
          "Score"),
        use_container_width=True
    )

with c4:
    st.plotly_chart(
        g(lstm_series, color(future,200,220),
          "LSTM Prediction",
          "Temperature (°C)"),
        use_container_width=True
    )