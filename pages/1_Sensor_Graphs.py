import streamlit as st
import pandas as pd
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
Sensor Monitoring & AI Insights
</div>
""", unsafe_allow_html=True)

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=2000, key="sensor_refresh")

# ---------- LOAD DATA ----------
data = pd.read_csv(os.path.join('data', 'sensor_data.csv'))

# ---------- SMOOTH SIMULATION ----------
recent_data, latest = get_smooth_data(data, key="sensor")

# ---------- SENSOR VALUES ----------
temp = latest['Temperature']
pressure = latest['Pressure']
vibration = latest['Vibration']
flow = latest['Current']

# ---------- COLOR ----------
def get_color(val, low, mid):
    if val <= low:
        return "green"
    elif val <= mid:
        return "yellow"
    else:
        return "red"

def flow_color(val):
    if val >= 20:
        return "green"
    elif val >= 10:
        return "yellow"
    else:
        return "red"

# ---------- GRAPH FUNCTION ----------
def graph(data, col, color, title, y_label):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=data[col],
        mode='lines',
        line=dict(color=color, width=3)
    ))

    fig.update_layout(
        height=200,
        title=title,
        template="plotly_dark",

        # ✅ AXIS LABELS
        xaxis_title="Time (Index)",
        yaxis_title=y_label,

        # ✅ REDUCE FLICKER
        yaxis=dict(
            range=[
                float(data[col].min()) * 0.95,
                float(data[col].max()) * 1.05
            ]
        ),

        margin=dict(l=10, r=10, t=30, b=10)
    )

    return fig

# =====================================================
# 🔴 SENSOR GRAPHS (2x2)
# =====================================================
c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        graph(recent_data, "Temperature",
              get_color(temp, 200, 220),
              "Temperature",
              "Temperature (°C)"),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        graph(recent_data, "Pressure",
              get_color(pressure, 160, 180),
              "Pressure",
              "Pressure (bar)"),
        use_container_width=True
    )

c3, c4 = st.columns(2)

with c3:
    st.plotly_chart(
        graph(recent_data, "Vibration",
              get_color(vibration, 1.2, 1.5),
              "Vibration",
              "Vibration (mm/s)"),
        use_container_width=True
    )

with c4:
    st.plotly_chart(
        graph(recent_data, "Current",
              flow_color(flow),
              "Flow",
              "Flow Rate (L/min)"),
        use_container_width=True
    )

# =====================================================
# 🤖 AI SUGGESTIONS
# =====================================================
st.subheader("AI Suggestions")

suggestions = []

def spike(series):
    return len(series) > 5 and abs(series.iloc[-1] - series.iloc[-5]) > 0.2 * series.mean()

# ---------- CONDITIONS ----------
if temp > 220:
    suggestions.append("🔴 High Temperature")
elif temp > 200:
    suggestions.append("🟡 Temperature Rising")

if pressure > 180:
    suggestions.append("🔴 High Pressure")
elif pressure > 160:
    suggestions.append("🟡 Pressure Rising")

if vibration > 1.5:
    suggestions.append("🔴 High Vibration")
elif vibration > 1.2:
    suggestions.append("🟡 Vibration Increasing")

if flow < 10:
    suggestions.append("🔴 Low Flow")
elif flow < 20:
    suggestions.append("🟡 Flow Dropping")

# ---------- SPIKE DETECTION ----------
if spike(recent_data["Temperature"]):
    suggestions.append("⚠️ Sudden Temperature Spike")

if spike(recent_data["Pressure"]):
    suggestions.append("⚠️ Sudden Pressure Spike")

# ---------- DISPLAY ----------
for s in suggestions:
    if "🔴" in s:
        st.error(s)
    elif "🟡" in s:
        st.warning(s)
    else:
        st.info(s)

if not suggestions:
    st.success("System Operating Normally")