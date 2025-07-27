import sys
sys.path.append('/opt/airflow/scripts')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from generate_fake_weather_csv import generate_fake_weather_csv

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

with DAG(
    dag_id='faker_csv_writer_dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *',
    catchup=False,
    description='Write fake weather data to CSV every minute'
) as dag:

    write_csv = PythonOperator(
        task_id='generate_fake_weather',
        python_callable=generate_fake_weather_csv
    )
