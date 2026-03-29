import pandas as pd
import random

data = []

for i in range(1, 5001):
    temperature = random.randint(20, 100)
    vibration = round(random.uniform(0.01, 1.5), 2)
    pressure = random.randint(90, 180)
    humidity = random.randint(30, 90)
    current = random.randint(5, 50)
    rpm = random.randint(500, 3000)
    voltage = random.randint(200, 260)
    sound = random.randint(30, 120)

    if temperature > 80 or vibration > 1.2 or pressure > 160 or current > 40:
        status = "Failure"
    elif temperature > 55 or vibration > 0.6 or pressure > 130 or current > 30:
        status = "Warning"
    else:
        status = "Normal"

    data.append([i, temperature, vibration, pressure, humidity, current, rpm, voltage, sound, status])

df = pd.DataFrame(data, columns=[
    "Time", "Temperature", "Vibration", "Pressure", "Humidity",
    "Current", "RPM", "Voltage", "Sound", "Machine_Status"
])

df.to_csv("data/sensor_data.csv", index=False)
print("Dataset generated successfully")