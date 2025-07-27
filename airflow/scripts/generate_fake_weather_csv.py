import csv
import os
from faker import Faker
import random
from datetime import datetime

fake = Faker()

def generate_fake_weather_csv():
    filename = "/opt/airflow/data/weather_iot_data.csv"

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Determine the starting ID
    id_counter = 1
    if os.path.exists(filename):
        with open(filename, mode='r') as existing_file:
            reader = csv.DictReader(existing_file)
            existing_ids = [int(row['id']) for row in reader if row.get('id', '').isdigit()]
            if existing_ids:
                id_counter = max(existing_ids) + 1

    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ['id', 'timestamp', 'name', 'city', 'temperature']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is new
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            writer.writeheader()

        for _ in range(3):
            writer.writerow({
                'id': id_counter,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'name': fake.name(),
                'city': fake.city(),
                'temperature': round(random.uniform(10, 40), 2)
            })
            id_counter += 1

    print(f"[FAKER] 3 rows appended to {filename}")

if __name__ == "__main__":
    generate_fake_weather_csv()
