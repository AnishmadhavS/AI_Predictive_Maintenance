import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(layout="wide")

# ---------- HEADER ----------
st.markdown("""
<div style="font-size:18px;font-weight:600;padding:10px;
background:#1f1f2e;border-radius:8px;margin-bottom:10px;">
Model Comparison
</div>
""", unsafe_allow_html=True)

# ---------- DATA ----------
df = pd.DataFrame({
    "Model":["Random Forest","LSTM","SVM","Decision Tree"],
    "Accuracy":[92,95,88,85],
    "Precision":[90,94,86,83],
    "Recall":[91,93,84,82]
})

df["Error"] = 100 - df["Accuracy"]

# ---------- GRAPH FUNCTION ----------
def bar(y, title, y_label):

    fig = px.bar(
        df,
        x="Model",
        y=y,
        text=y,
        color="Model"
    )

    fig.update_layout(
        height=220,
        title=title,
        template="plotly_dark",

        # ✅ AXIS LABELS
        xaxis_title="Machine Learning Models",
        yaxis_title=y_label,

        showlegend=False,

        margin=dict(l=10, r=10, t=40, b=10)
    )

    # Make text visible
    fig.update_traces(textposition="outside")

    return fig

# =====================================================
# 📊 2x2 LAYOUT
# =====================================================
c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        bar("Accuracy", "Model Accuracy Comparison", "Accuracy (%)"),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        bar("Error", "Model Error Rate Comparison", "Error Rate (%)"),
        use_container_width=True
    )

c3, c4 = st.columns(2)

with c3:
    st.plotly_chart(
        bar("Precision", "Model Precision Comparison", "Precision (%)"),
        use_container_width=True
    )

with c4:
    st.plotly_chart(
        bar("Recall", "Model Recall Comparison", "Recall (%)"),
        use_container_width=True
    )