import json
from airflow.providers.postgres.hooks.postgres import PostgresHook

class PostgresService:
    def __init__(self):
        self.pg_hook = PostgresHook(postgres_conn_id="currency_db")

    def execute(self, query:str, params:tuple|None = None):
        conn = self.pg_hook.get_conn();
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
            conn.commit()
        finally:
                cursor.close()
                conn.close()

    def fetchall(self, query:str, params:tuple|None = None):
        conn = self.pg_hook.get_conn();
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
                cursor.close()
                conn.close()