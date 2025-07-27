import json
import time
import requests
from kafka import KafkaProducer

def push_weather_to_kafka():
    API_KEY = "7f862b91dfe1c993e3c4a4408ace51b0"
    CITY = "Ahmedabad"
    KAFKA_TOPIC = "weather-topic"
    KAFKA_SERVER = "kafka:9092"

    # Initialize producer
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_SERVER],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "city": data["name"],
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "weather_description": data["weather"][0]["description"]
        }
        print(f"Sending: {weather_data}")
        producer.send(KAFKA_TOPIC, weather_data)
        producer.flush()
    else:
        print("Failed to fetch weather data")

