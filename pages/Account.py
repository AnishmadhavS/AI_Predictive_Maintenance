import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
.block-container {
    padding-top: 2.5rem;
}

/* Header */
.header-box {
    font-size:18px;
    font-weight:600;
    padding:10px;
    background:#1f1f2e;
    border-radius:8px;
    margin-bottom:12px;
}

/* Profile Card */
.profile-card {
    background:#26263a;
    padding:18px;
    border-radius:12px;
    margin-bottom:15px;
}

/* Titles */
.title {
    font-size:16px;
    font-weight:600;
    margin-bottom:6px;
}

.text {
    font-size:14px;
    margin-bottom:4px;
}

.section-title {
    font-size:15px;
    font-weight:600;
    margin-top:10px;
    margin-bottom:6px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header-box">Account & Governance</div>', unsafe_allow_html=True)

# =====================================================
# 🔹 USER PROFILE (FIXED CARD)
# =====================================================
with st.container():

    st.markdown('<div class="profile-card">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])

    with col1:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            width=90
        )

    with col2:
        st.markdown('<div class="title">Senior Safety Engineer</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Employee ID: 9999</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Role: Administrator</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Unit: Boiler #4</div>', unsafe_allow_html=True)
        st.markdown('<div class="text">Section: Burner B</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# 🔹 NOTIFICATION SETTINGS
# =====================================================
st.markdown('<div class="section-title">Notification Settings</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    sms = st.toggle("SMS Alerts", value=True)

with c2:
    email = st.toggle("Email Alerts", value=True)

if sms or email:
    st.success("Notifications Active")
else:
    st.warning("Notifications Disabled")

# =====================================================
# 🔹 AUDIT LOG (ONLY 5 ROWS)
# =====================================================
st.markdown('<div class="section-title">Audit Log</div>', unsafe_allow_html=True)

log_file = "employee_log.csv"

if os.path.exists(log_file):
    log_data = pd.read_csv(log_file)

    st.dataframe(
        log_data.tail(5),   # ✅ ONLY 5 ROWS
        use_container_width=True,
        height=180
    )
else:
    st.warning("No logs available")

# =====================================================
# 🔹 INCIDENT + ACTION PANEL
# =====================================================
col3, col4 = st.columns(2)

# ---------- INCIDENT ----------
with col3:
    st.markdown('<div class="section-title">Incident Details</div>', unsafe_allow_html=True)

    if os.path.exists(log_file) and not log_data.empty:

        select_col = "Timestamp" if "Timestamp" in log_data.columns else log_data.columns[0]

        incident = st.selectbox("Select Incident", log_data[select_col])

        row = log_data[log_data[select_col] == incident]

        st.info(row["Alert"].values[0] if "Alert" in row else "N/A")
        st.warning(row["Action"].values[0] if "Action" in row else "N/A")
        st.success(row["Status"].values[0] if "Status" in row else "N/A")

# ---------- ACTION PANEL ----------
with col4:
    st.markdown('<div class="section-title">Action Panel</div>', unsafe_allow_html=True)

    employee = st.selectbox(
        "Employee",
        ["Operator", "Maintenance", "Supervisor"]
    )

    instruction = st.text_input("Instruction")

    if st.button("Send Instruction"):
        if instruction.strip() == "":
            st.warning("Enter instruction")
        else:
            st.success(f"Sent to {employee}")

    if st.button("View Report"):
        st.info("""
        - AI detected anomaly  
        - Alert issued  
        - Maintenance performed  
        - System restored  
        """)