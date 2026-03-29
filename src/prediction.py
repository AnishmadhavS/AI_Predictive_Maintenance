import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

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

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Report
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))