import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load dataset
file_path = os.path.join('data', 'sensor_data.csv')
data = pd.read_csv(file_path)

dataset = data['Temperature'].values.reshape(-1, 1)

# Scale
scaler = MinMaxScaler()
dataset_scaled = scaler.fit_transform(dataset)

# Create sequences
X = []
y = []
seq_length = 20

for i in range(seq_length, len(dataset_scaled)):
    X.append(dataset_scaled[i-seq_length:i])
    y.append(dataset_scaled[i])

X = np.array(X)
y = np.array(y)

# LSTM Model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X, y, epochs=3, batch_size=32)

# Predict next value
last_seq = dataset_scaled[-20:]
last_seq = np.reshape(last_seq, (1, 20, 1))
predicted = model.predict(last_seq)
predicted = scaler.inverse_transform(predicted)

print("Future Temperature Prediction:", predicted[0][0])