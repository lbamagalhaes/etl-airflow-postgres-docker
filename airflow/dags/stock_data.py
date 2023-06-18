import logging
import os
from datetime import datetime, timedelta
import time

import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

# Configure Logging
log_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'load_csv_to_postgres.log')
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename=log_file_name
)


def get_latest_minute_data(api_key, symbol) -> None:
    interval = "1min"  # 1 minute interval

    # Fetch data from Alpha Vantage
    logging.info(f"Fetching data for symbol: {symbol}")
    ts = TimeSeries(key=api_key, output_format='pandas')

    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        try:
            data, meta_data = ts.get_intraday(symbol=symbol, interval=interval, outputsize='compact')
            logging.info(f"Data fetched successfully for symbol: {symbol}")
            break
        except Exception as e:
            logging.error(f"Error fetching data for symbol {symbol}: {e}")
            attempts += 1
            if attempts < max_attempts:
                logging.info(f"Waiting 1 minute before retrying...")
                time.sleep(60)
            else:
                logging.info(f"Max retry attempts reached. Skipping data retrieval for symbol {symbol}")
                return

    # Extract latest minute data
    latest_minute_data = data.tail(1)
    latest_minute_price = latest_minute_data['4. close'].values[0]
    latest_minute_timestamp = latest_minute_data.index[0]
    location_name  = meta_data['6. Time Zone']
    logging.info(f"Latest minute price for symbol {symbol}: {latest_minute_price}")

    # Check if data already exists in the database
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    query = f"SELECT * FROM stock_data WHERE symbol = '{symbol}' AND time = '{latest_minute_timestamp}'"
    result = pg_hook.get_records(query)

    if len(result) == 0:
        # Create DataFrame with relevant data
        df = pd.DataFrame(
            [[symbol, latest_minute_timestamp, latest_minute_price, 'USD', location_name]],
            columns=['symbol', 'time', 'price', 'currency', 'time_location']
        )

        # Write data to PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id='postgres')
        df.to_sql('stock_data', pg_hook.get_sqlalchemy_engine(), if_exists='append', index=False)
        logging.info("Data written to PostgreSQL")
    else:
        logging.info("Data already exists in the database. Skipping append.")


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
    'max_active_runs': 1
}

with DAG(
    'load_stock_data_to_postgres',
    default_args=default_args,
    description='Load CSV data into Postgres table',
    schedule_interval='* * * * *',
    catchup=False
) as dag:
    symbols = ['AAPL', 'MSFT', 'META', 'GOOGL', 'NVDA']

    for symbol in symbols:
        load_stock_data = PythonOperator(
            task_id=f'get_stock_data_{symbol}',
            python_callable=get_latest_minute_data,
            op_kwargs={
                'api_key': "GT497V1DZRV3ZFDN",
                'symbol': symbol
            }
        )

        load_stock_data
