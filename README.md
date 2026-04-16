# 🔥 AI Boiler Monitoring Dashboard

An AI-powered real-time monitoring system for industrial boiler sensors with predictive analytics, anomaly detection, and intelligent alerting.

---

## 📌 Project Overview

This project simulates a **real-time industrial boiler monitoring system** using sensor data and AI models. It provides:

- 📊 Live sensor visualization
- 🤖 AI-based predictions
- ⚠️ Automated alert system
- 👨‍🔧 Employee action tracking
- 📄 Audit & governance logs

---

## 🚀 Key Features

### 🔴 1. Real-Time Sensor Monitoring
- Temperature (°C)
- Pressure (bar)
- Vibration (mm/s)
- Flow Rate (L/min)
- Smooth real-time simulation using interpolation

---

### 🔵 2. AI Predictions
- Failure Probability (0–1 scale)
- Remaining Useful Life (Days)
- Anomaly Detection Score
- LSTM-based Future Prediction

---

### 🟡 3. Model Comparison
- Accuracy
- Precision
- Recall
- Error Rate
- Comparison of ML models:
  - Random Forest
  - LSTM
  - SVM
  - Decision Tree

---

### ⚠️ 4. Smart Alert System
- Detects abnormal conditions
- Sends alerts (Email enabled)
- Color-coded risk levels:
  - 🟢 Normal
  - 🟡 Warning
  - 🔴 Critical

---

### 👨‍🔧 5. Employee Action System
- Assign tasks to employees
- Log actions taken
- Track system recovery

---

### 📄 6. Governance & Audit Logs
- Timestamp-based logging
- AI recommendation tracking
- Human decision tracking
- Incident review system

---

## 🧠 Algorithms Used

- 📈 **LSTM (Long Short-Term Memory)**  
  Used for time-series prediction of future sensor values.

- 🌲 **Random Forest**  
  Used for classification and prediction.

- ⚡ **Anomaly Detection**  
  Identifies abnormal behavior in sensor data.

- 📊 **Failure Probability Model**  
  Weighted formula based on sensor conditions.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Visualization:** Plotly
- **Data Handling:** Pandas, NumPy
- **Simulation:** Custom interpolation logic
- **Alerts:** SMTP (Email)

---

## 📂 Project Structure
AI_Sensor_Project/
│
├── Dashboard.py
├── pages/
│ ├── 1_Sensor_Graphs.py
│ ├── 2_AI_Predictions.py
│ ├── 3_Model_Comparison.py
│ └── 4_Account.py
│
├── utils/
│ └── simulation.py
│
├── data/
│ └── sensor_data.csv
│
├── src/
│ └── email_alert.py
│
└── employee_log.csv


---

## ▶️ How to Run the Project

### 1️⃣ Install dependencies
```bash
pip install streamlit pandas plotly numpy

streamlit run Dashboard.py

http://localhost:8501
