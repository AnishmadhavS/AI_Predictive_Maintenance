import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Get current file directory
current_dir = os.path.dirname(__file__)

# Build path to dataset
file_path = os.path.join(current_dir, '..', 'data', 'sensor_data.csv')

# Load dataset
data = pd.read_csv(file_path)

print("Original Dataset:\n")
print(data.head())

# Convert Machine_Status to numbers
le = LabelEncoder()
data['Machine_Status'] = le.fit_transform(data['Machine_Status'])

print("\nAfter Label Encoding:\n")
print(data.head())

# Split features and target
X = data[['Temperature', 'Vibration', 'Pressure', 'Humidity']]
y = data['Machine_Status']

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print("\nData Preprocessing Completed")
print("Training Data Size:", len(X_train))
print("Testing Data Size:", len(X_test))