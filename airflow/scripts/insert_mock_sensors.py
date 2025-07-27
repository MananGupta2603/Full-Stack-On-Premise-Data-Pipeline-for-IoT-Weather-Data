import random
from faker import Faker
import mysql.connector
from datetime import datetime

fake = Faker()

def insert_mock_sensors():
    conn = mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="weatherdb"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iot_sensors (
            id INT AUTO_INCREMENT PRIMARY KEY,
            device_id VARCHAR(50),
            city VARCHAR(100),
            sensor_type VARCHAR(50),
            sensor_value FLOAT,
            registered_at DATETIME
        );
    """)

    sensor_types = ["temperature", "humidity", "pressure", "wind"]

    for _ in range(3):
        device_id = fake.uuid4()
        city = fake.city()
        sensor_type = random.choice(sensor_types)
        registered_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Generate appropriate value
        if sensor_type == "temperature":
            sensor_value = round(random.uniform(10.0, 45.0), 2)
        elif sensor_type == "humidity":
            sensor_value = round(random.uniform(20.0, 100.0), 2)
        elif sensor_type == "pressure":
            sensor_value = round(random.uniform(950.0, 1050.0), 2)
        elif sensor_type == "wind":
            sensor_value = round(random.uniform(0.0, 30.0), 2)

        cursor.execute("""
            INSERT INTO iot_sensors (device_id, city, sensor_type, sensor_value, registered_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (device_id, city, sensor_type, sensor_value, registered_at))

    conn.commit()
    cursor.close()
    conn.close()
    print("[MOCK] Inserted 3 enriched fake sensors.")
