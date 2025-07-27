
# 🌦️ Full-Stack On-Premise Data Pipeline for IoT & Weather Data

## 📌 Project Objective

The goal of this project is to build a production-grade, on-premise data engineering pipeline that ingests, processes, stores, and monitors real-time and historical weather data using open-source tools.

---

## 📈 Business Use Case

A hypothetical weather analytics company requires a data pipeline to:
- Ingest real-time weather data from external APIs
- Simulate synthetic IoT sensor data
- Process and transform data using batch and streaming methods
- Store the processed data for querying and analysis
- Monitor and automate the pipeline operations

---

## 🧰 Technologies & Tools Used

| Technology       | Purpose                          |
|------------------|----------------------------------|
| Python           | Scripting & Data Generation      |
| Apache Kafka     | Real-time Ingestion              |
| Apache Spark     | Streaming & Batch Processing     |
| Apache Hive      | Data Lake Table Storage          |
| MySQL            | Relational Data Storage          |
| Apache Airflow   | Workflow Orchestration           |
| Docker Compose   | Containerized Deployment         |


---

## 🏗️ Pipeline Architecture

```plaintext
        +-------------+         +---------+
        | Weather API | ----->  |  Kafka  |  ---> Spark Streaming ---> Parquet
        +-------------+         +---------+

        +-------------+                  +-------------------+
        | Faker CSV   | ----generate---> |   CSV Files       |
        +-------------+                  +-------------------+

        +-------------+                  +-------------------+
        | Faker MySQL | ----insert-----> |  MySQL (Raw Data) |
        +-------------+                  +-------------------+

                 CSV + MySQL  ---> Spark Batch ETL ---> Hive & Final MySQL Table

                   All jobs orchestrated via Apache Airflow
                  
````

---

## 🔁 Workflow Summary

### 1. **Ingestion**

* `weather_to_kafka_dag.py`: Pulls real-time weather data every minute → Kafka topic
* `faker_csv_dag.py`: Generates synthetic weather logs every minute into a CSV
* `mock_sensor_dag.py`: Inserts mock sensor/device data into MySQL

### 2. **Processing**

* `streaming_kafka_to_parquet.py`: Spark reads Kafka topic, writes Parquet every 5 min
* `batch_etl_to_hive_and_mysql.py`: Spark joins CSV + MySQL, transforms, and writes to Hive/MySQL

### 3. **Storage**

* **Hive Table**: Final structured output for queries
* **MySQL Table**: Final relational data for reporting
* **Parquet**: Raw real-time stream stored on disk

### 4. **Orchestration & Monitoring**

* Airflow DAGs handle scheduling and dependencies
* Grafana dashboards show health of Spark, Airflow, Docker services

---


## ✅ Prerequisites

* Docker & Docker Compose
* Python 3.x
* Java 8+
* Apache Spark (if running manually)
* Airflow installed (or run inside Docker)

---

## 🚀 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/MananGupta2603/Full-Stack-On-Premise-Data-Pipeline-for-IoT-Weather-Data
cd Full-Stack-On-Premise-Data-Pipeline-for-IoT-Weather-Data
```

2. **Start Docker Services**

```bash
docker-compose up -d
```

3. **Access Services**

* Airflow: `http://localhost:8080`
* MySQL: `localhost:3306`
* Hive: `localhost:10000` (via Beeline or JDBC)

4. **Trigger Airflow DAGs**

* `weather_to_kafka_dag` – fetches weather API to Kafka
* `batch_etl_dag` – runs ETL and writes to Hive/MySQL

---

## 📊 Example Data

### Weather API Data (from OpenWeatherMap):

```json
{
  "timestamp": "2025-07-27T12:00:00Z",
  "city": "Delhi",
  "temperature": 34.2,
  "humidity": 58,
  "weather_description": "clear sky"
}
```

### Faker CSV:

```csv
sensor_id,location,timestamp,temp_celsius,humidity_percent,rain_mm
101,"Chennai","2025-07-27 12:01:00",31.5,60,2.4
```

---

## 🧪 Testing

* Validate Spark jobs by checking Parquet files and Hive/SQL table outputs
* Check Airflow DAG logs for execution status
* Monitor container and job health using Grafana dashboards

---

## 🏁 Deliverables

* Airflow DAGs: `weather_to_kafka_dag.py`, `faker_csv_dag.py` and `mock_sensor_dag.py`
* Spark Jobs: `streaming_kafka_to_parquet.py`, `batch_etl_to_hive_and_mysql.py`
* Faker Scripts: `generate_fake_weather_csv.py`, `insert_mock_sensors.py`
* Docker Compose File
* SQL Scripts (Hive Table)
* README.md


---

## 📚 Key Learnings

* Building real-time and batch data pipelines using Apache Spark
* Ingesting and simulating data from multiple sources (API, Faker, DB)
* Using Airflow for orchestration
* End-to-end Dockerized deployment of a data engineering project

---

