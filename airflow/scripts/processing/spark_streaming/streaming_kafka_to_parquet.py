
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StringType, FloatType

# Define JSON schema
schema = StructType() \
    .add("timestamp", StringType()) \
    .add("city", StringType()) \
    .add("lat", FloatType()) \
    .add("lon", FloatType()) \
    .add("temperature", FloatType()) \
    .add("humidity", FloatType()) \
    .add("pressure", FloatType()) \
    .add("wind_speed", FloatType()) \
    .add("weather_description", StringType())


print("-------->Creating Spark session...")

spark = SparkSession.builder \
    .appName("KafkaToParquetStream") \
    .getOrCreate()

print("--------->Spark session created.")
spark.sparkContext.setLogLevel("WARN")

# Reading from Kafka
print("--------->Subscribing to Kafka topic 'weather-topic'...")
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather-topic") \
    .option("startingOffsets", "earliest")\
    .option("failOnDataLoss", "false").load()

print("--------->Kafka source initialized.")

# Raw Kafka messages to console
print("---------->Starting raw Kafka stream to console...")
df_kafka.selectExpr("CAST(value AS STRING)").writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .trigger(processingTime="10 seconds") \
    .start()

# Parsing JSON
print("--------->Parsing Kafka JSON messages...")
df_json = df_kafka.selectExpr("CAST(value AS STRING) as json_string") \
    .select(from_json(col("json_string"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("processing_timestamp", current_timestamp())

# Print parsed JSON to console
print("---------->Starting parsed JSON stream to console...")
df_json.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .trigger(processingTime="10 seconds") \
    .start()

# Write to Parquet
print("---------->Writing stream to local Parquet at /opt/airflow/data/weather_parquet...")
df_json.writeStream \
    .format("parquet") \
    .outputMode("append") \
    .option("path", "file:///opt/airflow/data/weather_parquet") \
    .option("checkpointLocation", "file:///opt/airflow/data/weather_parquet_checkpoint") \
    .trigger(processingTime="1 minute") \
    .start() \
    .awaitTermination()

print("---------> Streaming job started and running.")