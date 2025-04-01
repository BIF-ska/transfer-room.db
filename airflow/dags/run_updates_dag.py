from airflow import DAG
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from python_code.services.runallupdates import run_all_updates




default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='daily_db_updates',
    default_args=default_args,
    description='Run update script once per day',
    schedule_interval='0 0 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    run_updates = PythonOperator(
        task_id='run_all_updates',
        python_callable=run_all_updates,
    )

    run_updates