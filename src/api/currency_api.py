import logging
from .base_api import BaseAPI


class CurrencyAPI(BaseAPI):
    BASE_URL = "https://api.frankfurter.dev/v2"

    def __init__(self):
        super().__init__(self.BASE_URL)

    def get_rates(self, base_currency:str = 'TRY', target_currency:list|None = None):

        quotes_params = ','.join(target_currency) if target_currency else None
        return self._request(
            method = 'GET',
            endpoint = 'rates',
            params = {
                "base": base_currency,
                "quotes": quotes_params
            }
        )
