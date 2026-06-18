import json
from .postgress_service import PostgresService

class RowDataSaver:
    def __init__(self):
         self.db = PostgresService()

    def run(self, data:dict):
        return self.db.execute(
            "INSERT INTO currency.raw_data (data) VALUES (%s)",
            (json.dumps(data),)
        )
    

    
     