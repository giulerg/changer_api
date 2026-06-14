from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from src.services.extractor import Extractor

with DAG(
    dag_id = "currency_dag",
    start_date=datetime(2026,1,1),
    schedule="@daily"
) as dag:
     
    def load_raw():
        pass
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=Extractor.run()
    )
    load_raw_task = PythonOperator(
        task_id = "load_raw",
        python_callable = load_raw
    )
extract_task >> load_raw_task

# extract
# load_raw
# ttansform
# detect_anomalies
