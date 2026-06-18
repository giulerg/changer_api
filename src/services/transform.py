import json
import logging
from .postgress_service import PostgresService

logger = logging.getLogger(__name__)


class Transform:
    def __init__(self):
        self.db = PostgresService()

    def run(self):
        rows = self.db.fetchall(
            "SELECT id, data FROM currency.raw_data WHERE status = 'NEW'"
        )
        last_id = None

        try:
            for last_id, data in rows:
                transformed_data = self.transform_data(data)

                for record in transformed_data:
                    self.db.execute(
                        """
                        INSERT INTO currency.transformed_data
                            (main_currency, currency, rate, date)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (record["main_currency"], record["currency"],
                         record["rate"], record["date"]),
                    )

                self.db.execute(
                    "UPDATE currency.raw_data SET data = %s, status = 'PROCESSED' WHERE id = %s",
                    (json.dumps(transformed_data), last_id),
                )

        except Exception as e:
            logger.error("Transform failed on raw_data id=%s: %s", last_id, e)
            if last_id is not None:
                self.db.execute(
                    "UPDATE currency.raw_data SET status = 'ERROR' WHERE id = %s",
                    (last_id,),
                )
            raise

    def transform_data(self, row_data):
        transformed = []

        for row in row_data:
            main_currency = row.get("base")
            currency = row.get("quote")
            rate = row.get("rate")
            date = row.get("date")

            inverted_rate = round(1 / rate, 4) if rate else 0  # ← внутри цикла

            transformed.append(
                {
                    "main_currency": main_currency,
                    "currency": currency,
                    "rate": inverted_rate,
                    "date": date,
                }
            )

        return transformed