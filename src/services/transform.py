import logging
from .postgress_service import PostgresService

class Transform:
    def __init__(self):
        self.db = PostgresService()
    
    def run(self):
        rows = self.db.fetchall("SELECT id, data FROM currency.raw_data WHERE status = 'NEW'")
        last_id = None

        try:
            for row in rows:
                last_id, data = row
                transformed_data = self.transform_data(data)
                
                for row in transformed_data:
                    self.db.execute(
                    "INSERT INTO currency.transformed_data (main_currency, currency, rate, date) VALUES (%s, %s, %s, %s)",
                        (transformed_data["main_currency"], transformed_data["currency"], transformed_data["rate"], transformed_data["date"])
                )

                self.db.execute(
                    "UPDATE currency.raw_data SET data = %s, status = 'PROCESSED' WHERE id = %s",
                    (transformed_data, last_id)
            )
        except Exception as e:
            if last_id is not None:
                self.db.execute(
                    "UPDATE currency.raw_data SET status = 'ERROR' WHERE id = %s",
                    (last_id,)
                )
            raise 

    def transform_data(self, row_data):
    
        transformed = []

        for row in row_data:
            main_currency = row.get("base")
            currency = row.get("quote")    
            rate = row.get("rate")
            date = row.get("date")
        
        if rate is not None and rate != 0:
            inverted_rate = round(1 / rate, 4)
        else:
            inverted_rate = 0


        transformed.append(
            {
                "main_currency": main_currency,
                "rate": inverted_rate, 
                "date": date,
                "currency": currency,
            }
        )


      

        return transformed
    