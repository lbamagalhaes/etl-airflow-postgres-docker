
import pandas as pd
import logging
import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

from cosmos.providers.dbt.task_group import DbtTaskGroup


script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))

path = parent_dir + '/data/input.csv'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Set the desired log file name
log_file_name = parent_dir + '/logs/load_csv_to_postgres.log'

# Configure the logging format and file name
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=log_file_name
)

def load_csv_to_postgres():
    logging.info("Starting load_csv_to_postgres task")
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    logging.info("Reading CSV file")
    df = pd.read_csv(path)
    logging.info("Loaded CSV file successfully")
    logging.info("Writing data to Postgres")
    df.to_sql('my_table', pg_hook.get_sqlalchemy_engine(), if_exists='append', index=False)
    logging.info("Data written to Postgres successfully")


with DAG(
    'load_csv_to_postgres',
    default_args=default_args,
    description='Load CSV data into Postgres table',
    schedule_interval=None,
) as dag:


    load_csv_task = PythonOperator(
        task_id='load_csv_to_postgres',
        python_callable=load_csv_to_postgres
    )

    calculate_avg = DbtTaskGroup(
            dbt_root_path="/opt/dbt",
            dbt_project_name="airflow",
            conn_id="postgres",
            profile_args={
                "schema": "public",
            },
        )

load_csv_task >> calculate_avg