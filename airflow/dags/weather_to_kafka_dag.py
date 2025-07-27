
import sys
sys.path.append('/opt/airflow/scripts')
from weather_producer import push_weather_to_kafka
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='weather_to_kafka_dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *',
    catchup=False,
    description='Push weather data to Kafka every minute'
) as dag:

    push_weather = PythonOperator(
        task_id='push_weather_to_kafka',
        python_callable=push_weather_to_kafka
    )
