import sqlite3

conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    time INTEGER,
    temperature REAL,
    vibration REAL,
    pressure REAL,
    humidity REAL,
    current REAL,
    rpm REAL,
    voltage REAL,
    sound REAL,
    status TEXT,
    risk REAL,
    rul REAL
)
""")

conn.commit()
conn.close()

print("Database created")