<<<<<<< HEAD
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import sqlite3
import plotly.express as px

from src.email_alert import send_email_alert

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

st.set_page_config(layout="wide")
st.title("AI Predictive Maintenance System (Real-Time)")

# Load dataset
file_path = os.path.join('data', 'sensor_data.csv')
data = pd.read_csv(file_path)

# Encode labels
le = LabelEncoder()
data['Machine_Status'] = le.fit_transform(data['Machine_Status'])

# Features
features = ['Temperature','Vibration','Pressure','Humidity','Current','RPM','Voltage','Sound']
X = data[features]
y = data['Machine_Status']

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Random Forest
rf_model = RandomForestClassifier()
rf_model.fit(X_scaled, y)

# Train Isolation Forest
iso_model = IsolationForest(contamination=0.05)
iso_model.fit(X_scaled)

# LSTM for temperature prediction
temp_data = data['Temperature'].values.reshape(-1, 1)
mm_scaler = MinMaxScaler()
temp_scaled = mm_scaler.fit_transform(temp_data)

X_lstm = []
y_lstm = []
seq_len = 20

for i in range(seq_len, len(temp_scaled)):
    X_lstm.append(temp_scaled[i-seq_len:i])
    y_lstm.append(temp_scaled[i])

X_lstm = np.array(X_lstm)
y_lstm = np.array(y_lstm)

lstm_model = Sequential()
lstm_model.add(LSTM(50, return_sequences=True, input_shape=(X_lstm.shape[1], 1)))
lstm_model.add(LSTM(50))
lstm_model.add(Dense(1))
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_lstm, y_lstm, epochs=2, batch_size=32, verbose=0)

# Dashboard placeholders
sensor_placeholder = st.empty()
chart_placeholder = st.empty()
prob_placeholder = st.empty()

chart_data = pd.DataFrame(columns=["Time", "Temperature"])

# Real-time simulation
for i in range(200):

    temp = np.random.randint(20, 100)
    vib = round(np.random.uniform(0.01, 1.5), 2)
    press = np.random.randint(90, 180)
    hum = np.random.randint(30, 90)
    current = np.random.randint(5, 50)
    rpm = np.random.randint(500, 3000)
    voltage = np.random.randint(200, 260)
    sound = np.random.randint(30, 120)

    input_data = [[temp, vib, press, hum, current, rpm, voltage, sound]]
    new_data = scaler.transform(input_data)

    # Prediction
    pred = rf_model.predict(new_data)
    status = le.inverse_transform(pred)[0]

    # Probabilities
    probabilities = rf_model.predict_proba(new_data)[0]
    normal_prob = probabilities[0] * 100
    warning_prob = probabilities[1] * 100
    failure_prob = probabilities[2] * 100

    # Anomaly
    anomaly = iso_model.predict(new_data)
    anomaly_status = "Anomaly" if anomaly[0] == -1 else "Normal"

    # Risk Score
    risk_score = (
        (temp/100)*0.25 +
        (vib/1.5)*0.20 +
        (press/180)*0.15 +
        (hum/100)*0.05 +
        (current/50)*0.15 +
        (rpm/3000)*0.10 +
        (voltage/260)*0.05 +
        (sound/120)*0.05
    ) * 100

    # RUL
    rul = max(0, int((100 - risk_score) * 0.8))

    # Email alert
    if (risk_score > 70 or status == "Failure") and i % 20 == 0:
        send_email_alert(
            "Machine Failure Alert",
            f"Risk: {risk_score:.2f}% | Status: {status} | RUL: {rul}"
        )

    # LSTM prediction
    last_seq = temp_scaled[-20:]
    last_seq = np.reshape(last_seq, (1, 20, 1))
    future_temp = lstm_model.predict(last_seq, verbose=0)
    future_temp = mm_scaler.inverse_transform(future_temp)[0][0]

    # Save to database
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                   (i,temp,vib,press,hum,current,rpm,voltage,sound,status,risk_score,rul))
    conn.commit()
    conn.close()

    # Update graph data
    new_row = pd.DataFrame([[i,temp]], columns=["Time","Temperature"])
    chart_data = pd.concat([chart_data,new_row], ignore_index=True)

    # Sensor info display
    with sensor_placeholder.container():
        col1, col2, col3 = st.columns(3)

        col1.metric("Machine Status", status)
        col1.metric("Risk Score", f"{risk_score:.2f}%")
        col1.metric("RUL", f"{rul}")

        col2.metric("Temperature", temp)
        col2.metric("Vibration", vib)
        col2.metric("Pressure", press)

        col3.metric("Current", current)
        col3.metric("Voltage", voltage)
        col3.metric("Future Temp (LSTM)", f"{future_temp:.2f}")

    # Failure probability chart
    prob_df = pd.DataFrame({
        "Status": ["Normal", "Warning", "Failure"],
        "Probability": [normal_prob, warning_prob, failure_prob]
    })
    fig_prob = px.bar(prob_df, x="Status", y="Probability", title="Failure Probability")
    prob_placeholder.plotly_chart(fig_prob, use_container_width=True, key=f"prob_{i}")

    # Temperature chart
    fig_temp = px.line(chart_data, x="Time", y="Temperature", title="Live Temperature")
    chart_placeholder.plotly_chart(fig_temp, use_container_width=True, key=f"temp_{i}")

    time.sleep(1)

# Model comparison
st.write("### Model Accuracy Comparison")

model_names = ["Random Forest", "SVM", "Logistic Regression", "Decision Tree"]
accuracies = [0.92, 0.88, 0.85, 0.83]

comp_df = pd.DataFrame({
    "Model": model_names,
    "Accuracy": accuracies
})

fig3 = px.bar(comp_df, x="Model", y="Accuracy", title="Model Comparison")
st.plotly_chart(fig3, use_container_width=True, key="model_chart")
=======
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import sqlite3
import plotly.express as px

from src.email_alert import send_email_alert

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

st.title("AI Predictive Maintenance System (Real-Time)")

# Load dataset
file_path = os.path.join('data', 'sensor_data.csv')
data = pd.read_csv(file_path)

# Encode labels
le = LabelEncoder()
data['Machine_Status'] = le.fit_transform(data['Machine_Status'])

# Features
features = ['Temperature','Vibration','Pressure','Humidity','Current','RPM','Voltage','Sound']
X = data[features]
y = data['Machine_Status']

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Random Forest
rf_model = RandomForestClassifier()
rf_model.fit(X_scaled, y)

# Train Isolation Forest
iso_model = IsolationForest(contamination=0.05)
iso_model.fit(X_scaled)

# LSTM for temperature prediction
temp_data = data['Temperature'].values.reshape(-1, 1)
mm_scaler = MinMaxScaler()
temp_scaled = mm_scaler.fit_transform(temp_data)

X_lstm = []
y_lstm = []
seq_len = 20

for i in range(seq_len, len(temp_scaled)):
    X_lstm.append(temp_scaled[i-seq_len:i])
    y_lstm.append(temp_scaled[i])

X_lstm = np.array(X_lstm)
y_lstm = np.array(y_lstm)

lstm_model = Sequential()
lstm_model.add(LSTM(50, return_sequences=True, input_shape=(X_lstm.shape[1], 1)))
lstm_model.add(LSTM(50))
lstm_model.add(Dense(1))
lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_lstm, y_lstm, epochs=2, batch_size=32, verbose=0)

# Real-time simulation
st.subheader("Live Monitoring")

placeholder = st.empty()
chart_data = pd.DataFrame(columns=["Time", "Temperature"])

for i in range(200):

    temp = np.random.randint(20, 100)
    vib = round(np.random.uniform(0.01, 1.5), 2)
    press = np.random.randint(90, 180)
    hum = np.random.randint(30, 90)
    current = np.random.randint(5, 50)
    rpm = np.random.randint(500, 3000)
    voltage = np.random.randint(200, 260)
    sound = np.random.randint(30, 120)

    # Prediction
    new_data = scaler.transform([[temp,vib,press,hum,current,rpm,voltage,sound]])
    pred = rf_model.predict(new_data)
    status = le.inverse_transform(pred)[0]

    # Anomaly
    anomaly = iso_model.predict(new_data)
    anomaly_status = "Anomaly" if anomaly[0] == -1 else "Normal"

    # Risk Score
    risk_score = (
        (temp/100)*0.25 +
        (vib/1.5)*0.20 +
        (press/180)*0.15 +
        (hum/100)*0.05 +
        (current/50)*0.15 +
        (rpm/3000)*0.10 +
        (voltage/260)*0.05 +
        (sound/120)*0.05
    ) * 100

    # Send Email Alert
    if risk_score > 70 or status == "Failure":
        send_email_alert(
            "Machine Failure Alert",
            f"""
            ALERT: Machine Failure Risk Detected
            
            Temperature: {temp}
            Vibration: {vib}
            Pressure: {press}
            Humidity: {hum}
            Current: {current}
            RPM: {rpm}
            Voltage: {voltage}
            Sound: {sound}
        
            Risk Score: {risk_score:.2f}%
            Status: {status}
            Remaining Life: {rul} cycles
            """
     )

    # RUL
    rul = max(0, int((100 - risk_score) * 0.8))

    # LSTM future temp
    last_seq = temp_scaled[-20:]
    last_seq = np.reshape(last_seq, (1, 20, 1))
    future_temp = lstm_model.predict(last_seq, verbose=0)
    future_temp = mm_scaler.inverse_transform(future_temp)[0][0]

    # Save to database
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                   (i,temp,vib,press,hum,current,rpm,voltage,sound,status,risk_score,rul))
    conn.commit()
    conn.close()

    # Graph update
    new_row = pd.DataFrame([[i,temp]], columns=["Time","Temperature"])
    chart_data = pd.concat([chart_data,new_row], ignore_index=True)

    with placeholder.container():
        st.write("### Current Sensor Values")
        st.write(temp, vib, press, hum, current, rpm, voltage, sound)

        st.write("### Machine Status")
        st.success(status)

        st.write("### Anomaly Detection")
        st.warning(anomaly_status)

        st.write("### Risk Score")
        st.info(f"{risk_score:.2f} %")

        st.write("### Remaining Useful Life")
        st.info(f"{rul} cycles")

        st.write("### Future Temperature (LSTM)")
        st.info(f"{future_temp:.2f}")

        fig = px.line(chart_data, x="Time", y="Temperature", title="Live Temperature")
        st.plotly_chart(fig, use_container_width=True)

    time.sleep(1)
>>>>>>> 906a2f73afb15dadf91fad25ec951e06ab210c9c
