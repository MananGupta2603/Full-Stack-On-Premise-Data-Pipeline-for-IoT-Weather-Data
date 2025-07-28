from pyspark.sql import SparkSession

# Initialize SparkSession with Hive support
spark = SparkSession.builder \
    .appName("BatchETL_CSV_MySQL_To_HiveAndMySQL") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

# -------------------------------
# Step 1: Read CSV File (IoT)
# -------------------------------
df_csv = spark.read.csv("file:///opt/airflow/data/weather_iot_data.csv", header=True, inferSchema=True)

# -------------------------------
# Step 2: Read MySQL Table
# -------------------------------
df_mysql = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql:3306/weatherdb") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "iot_sensors") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

# -------------------------------
# Step 3: Transform (Join + Select)
# -------------------------------
# Example: Join on city and filter where temp > 25
df_joined = df_csv.join(df_mysql, on="id", how="inner") \
    .filter(df_csv.temperature > 20) \
    .select(
        df_csv.timestamp.alias("iot_time"),
        df_csv.name,
        df_csv.city,
        df_csv.temperature.alias("iot_temp"),
        df_mysql.device_id,
        df_mysql.sensor_type,
        df_mysql.sensor_value.alias("mysql_sensor_value")
    )

print(f"Row count in final DataFrame: {df_joined.count()}")
df_joined.show()
# -------------------------------
# Step 4A: Save to Hive Table
# -------------------------------

# Now save to Hive
df_joined.write.mode("overwrite").saveAsTable("final_table")

# -------------------------------
# Step 4B: Save to MySQL Table
# -------------------------------
df_joined.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://mysql:3306/weatherdb") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("dbtable", "final_table") \
    .option("user", "root") \
    .option("password", "root") \
    .mode("overwrite") \
    .save()

print("ETL Completed: Final table written to Hive and MySQL.")
