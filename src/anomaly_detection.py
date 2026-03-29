import pandas as pd
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'data', 'sensor_data.csv')
data = pd.read_csv(file_path)

# Encode Machine_Status
le = LabelEncoder()
data['Machine_Status'] = le.fit_transform(data['Machine_Status'])

# Features
X = data[['Temperature', 'Vibration', 'Pressure', 'Humidity']]

# Scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Isolation Forest Model
model = IsolationForest(contamination=0.3)
data['Anomaly'] = model.fit_predict(X_scaled)

# Convert output
data['Anomaly'] = data['Anomaly'].map({1: 'Normal', -1: 'Anomaly'})

print(data[['Temperature', 'Vibration', 'Pressure', 'Humidity', 'Anomaly']])