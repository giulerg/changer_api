from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import datetime
import logging

from src.services.extractor import Extractor
from src.services.row_data_saver import RowDataSaver
 

with DAG(
    dag_id = "currency_dag",
    start_date=datetime(2026,1,1),
    schedule="@daily"
) as dag:
    
    @task(task_id="extract")
    def extract():
        logging.info("Начинаю загрузку данных")
        extractor = Extractor()
        data = extractor.run()
        logging.info("Загрузка данных завершена")
        return data
    
    @task(task_id="load_raw")
    def load_raw(data:dict|None):
        return RowDataSaver().run(data)

    
    extract_task = extract()
    load_raw_task = load_raw(extract_task)

    extract_task >> load_raw_task
# extract
# load_raw
# ttansform
# detect_anomalies
