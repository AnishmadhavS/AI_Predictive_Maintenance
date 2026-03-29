import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load dataset
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, '..', 'data', 'sensor_data.csv')
data = pd.read_csv(file_path)

# Encode labels
le = LabelEncoder()
data['Machine_Status'] = le.fit_transform(data['Machine_Status'])

# Features and target
X = data[['Temperature', 'Vibration', 'Pressure', 'Humidity']]
y = data['Machine_Status']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = RandomForestClassifier()
model.fit(X_scaled, y)

# New sensor input (example)
new_data = [[85, 1.3, 165, 78]]  # Temperature, Vibration, Pressure, Humidity
new_data_scaled = scaler.transform(new_data)

# Predict
prediction = model.predict(new_data_scaled)
status = le.inverse_transform(prediction)

print("Predicted Machine Status:", status[0])

# Decision Support Logic
if status[0] == "Normal":
    print("Recommendation: Machine is operating normally. No action required.")
elif status[0] == "Warning":
    print("Recommendation: Schedule maintenance soon.")
else:
    print("Recommendation: High failure risk! Stop machine and perform maintenance immediately.")