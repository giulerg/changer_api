from src.api.currency_api import CurrencyAPI

class Extractor:
    def __init__(self):
        self.api = CurrencyAPI()

    def run(self, base_currency:str = 'TRY', target_currency:list|None = None):
        return self.api.get_rates(base_currency, target_currency)