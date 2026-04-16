import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np
from streamlit_autorefresh import st_autorefresh
from utils.simulation import get_smooth_data
from src.email_alert import send_email_alert

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide")

st.markdown("""
<div style="font-size:18px;font-weight:600;padding:10px;
background:#1f1f2e;border-radius:8px;margin-bottom:10px;">
Dashboard
</div>
""", unsafe_allow_html=True)

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=2000, key="refresh")

# ---------- LOAD DATA ----------
data = pd.read_csv(os.path.join('data', 'sensor_data.csv'))

# ---------- SMOOTH SIMULATION ----------
recent_data, latest = get_smooth_data(data, key="dashboard")

# ---------- SENSOR VALUES ----------
temp = latest['Temperature']
pressure = latest['Pressure']
vibration = latest['Vibration']
flow = latest['Current']

# ---------- STATUS ----------
if temp > 220:
    status = "HIGH TEMPERATURE"
elif pressure > 180:
    status = "HIGH PRESSURE"
elif vibration > 1.5:
    status = "HIGH VIBRATION"
elif flow < 10:
    status = "LOW FLOW"
else:
    status = "NORMAL"

# ---------- METRICS ----------
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Temperature (°C)", round(temp,2))
c2.metric("Pressure (bar)", round(pressure,2))
c3.metric("Vibration (mm/s)", round(vibration,2))
c4.metric("Flow (L/min)", round(flow,2))
c5.metric("Status", status)

# ---------- COLOR ----------
def color(val, low, mid):
    if val <= low: return "green"
    elif val <= mid: return "yellow"
    else: return "red"

def flow_color(val):
    if val >= 20: return "green"
    elif val >= 10: return "yellow"
    else: return "red"

# ---------- SENSOR GRAPH FUNCTION ----------
def graph(data, col, color, title, y_label):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=data[col],
        mode='lines',
        line=dict(color=color,width=3)
    ))

    fig.update_layout(
        height=200,
        title=title,
        template="plotly_dark",

        # ✅ AXIS LABELS
        xaxis_title="Time (Index)",
        yaxis_title=y_label,

        # ✅ FIX FLICKER
        yaxis=dict(
            range=[
                float(data[col].min()) * 0.95,
                float(data[col].max()) * 1.05
            ]
        ),

        margin=dict(l=10,r=10,t=30,b=10)
    )

    return fig

# =====================================================
# 🔴 SENSOR GRAPHS
# =====================================================
st.subheader("Sensor Monitoring")

c1,c2 = st.columns(2)
with c1:
    st.plotly_chart(graph(recent_data,"Temperature",color(temp,200,220),"Temperature","Temperature (°C)"), use_container_width=True)
with c2:
    st.plotly_chart(graph(recent_data,"Pressure",color(pressure,160,180),"Pressure","Pressure (bar)"), use_container_width=True)

c3,c4 = st.columns(2)
with c3:
    st.plotly_chart(graph(recent_data,"Vibration",color(vibration,1.2,1.5),"Vibration","Vibration (mm/s)"), use_container_width=True)
with c4:
    st.plotly_chart(graph(recent_data,"Current",flow_color(flow),"Flow","Flow Rate (L/min)"), use_container_width=True)

# =====================================================
# 🔵 AI GRAPHS
# =====================================================
st.subheader("AI Predictions")

# AI calculations
fp = (temp/250)*0.4 + (pressure/200)*0.3 + (vibration/2)*0.2 + (flow/100)*0.1
rul = int((1-fp)*100)
anomaly = vibration*0.5 + temp*0.3
future = temp + np.random.uniform(-5,10)

# ---------- AI GRAPH FUNCTION ----------
def ai_graph(series, col, title, y_label):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=series,
        mode='lines',
        line=dict(color=col,width=3)
    ))

    fig.update_layout(
        height=200,
        title=title,
        template="plotly_dark",

        # ✅ AXIS LABELS
        xaxis_title="Time",
        yaxis_title=y_label,

        margin=dict(l=10,r=10,t=30,b=10)
    )

    return fig

# ---------- SERIES ----------
fp_series = np.linspace(0.1, fp, 50)
rul_series = np.linspace(rul, 0, 50)
an_series = np.linspace(20, anomaly, 50)
lstm_series = np.linspace(temp, future, 50)

# ---------- DISPLAY ----------
c5,c6 = st.columns(2)
with c5:
    st.plotly_chart(ai_graph(fp_series, "red", "Failure Probability", "Probability (0-1)"), use_container_width=True)
with c6:
    st.plotly_chart(ai_graph(rul_series, "green", "Remaining Useful Life", "Days"), use_container_width=True)

c7,c8 = st.columns(2)
with c7:
    st.plotly_chart(ai_graph(an_series, "orange", "Anomaly Score", "Score"), use_container_width=True)
with c8:
    st.plotly_chart(ai_graph(lstm_series, "blue", "LSTM Prediction", "Temperature (°C)"), use_container_width=True)

# =====================================================
# ⚠️ ALERT PANEL
# =====================================================
st.subheader("Alert Panel")

if status != "NORMAL":
    st.error(status)

    if st.button("Send Email Alert"):
        send_email_alert(
            subject="Boiler Alert",
            message=f"{status} detected. Immediate action required."
        )
        st.success("Email Sent")
else:
    st.success("System Normal")

# =====================================================
# 👷 EMPLOYEE ACTION
# =====================================================
st.subheader("Employee Action")

employee = st.selectbox("Select Employee", ["Operator","Maintenance","Supervisor"])

if st.button("Send Message"):
    st.success(f"Message sent to {employee}")

action = st.text_input("Action Taken")

if st.button("Log Action"):
    df = pd.DataFrame([{
        "Timestamp": pd.Timestamp.now(),
        "Alert": status,
        "Recommendation": status,
        "Employee": employee,
        "Action": action,
        "Status": "Resolved"
    }])

    file = "employee_log.csv"

    if os.path.exists(file):
        df.to_csv(file, mode='a', header=False, index=False)
    else:
        df.to_csv(file, index=False)

    st.success("Logged Successfully")

# =====================================================
# 📄 AUDIT LOG
# =====================================================
st.subheader("Audit Log")

file = "employee_log.csv"

if os.path.exists(file):
    log = pd.read_csv(file)
    st.dataframe(log.tail(10), use_container_width=True)
else:
    st.warning("No logs yet")