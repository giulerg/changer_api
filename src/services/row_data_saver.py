import json
from airflow.providers.postgres.hooks.postgres import PostgresHook

class RowDataSaver:
    def run(self, data:dict):
        pg_hook = PostgresHook(postgres_conn_id="currency_db")
        conn = pg_hook.get_conn();
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO currency.raw_data (data) VALUES (%s)", 
                    (json.dumps(data),)
                )
            conn.commit()
        finally:
                cursor.close()
                conn.close()