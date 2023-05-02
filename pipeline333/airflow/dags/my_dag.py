from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from data_ingestion import get_weather_forecast
from data_transformation import extract_features
from data_plotting import plot_weather_data
from data_psql import write_to_psql
import log


logger = log.get_logger('log')
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 30),
    'retries': 0
}

with DAG('weather_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    t1 = PythonOperator(
        task_id='get_weather_forecast',
        python_callable=get_weather_forecast,
        op_kwargs={'logger': logger}
    )

    t2 = PythonOperator(
        task_id='extract_features',
        python_callable=extract_features,
        op_kwargs={'logger': logger}
    )

    t3 = PythonOperator(
        task_id='plot_weather_data',
        python_callable=plot_weather_data,
        op_kwargs={'logger': logger}
    )

    t4 = PythonOperator(
        task_id='write_to_psql',
        python_callable=write_to_psql,
        op_kwargs={'logger': logger}
    )

    # so that t3 or t4 can be run in any order after t2
    t3_t4 = DummyOperator(task_id='t3_t4')

    t1 >> t2 >> t3_t4
    t3_t4 >> [t3, t4]
