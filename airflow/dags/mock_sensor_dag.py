import sys
sys.path.append('/opt/airflow/scripts')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from insert_mock_sensors import insert_mock_sensors

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

with DAG(
    dag_id='mock_sensor_data_dag',
    default_args=default_args,
    schedule_interval='*/1 * * * *',  # change to '*/10 * * * *' to run every 10 minutes
    catchup=False,
    description='Insert fake IoT sensor data into MySQL using Faker'
) as dag:

    insert_sensors = PythonOperator(
        task_id='insert_mock_sensors',
        python_callable=insert_mock_sensors
    )
