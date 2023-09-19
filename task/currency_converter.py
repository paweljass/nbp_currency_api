from dataclasses import dataclass
import dataclasses
import requests
from datetime import datetime
import config
import json
from connectors.database.json import JsonFileDatabaseConnector
from connectors.database.sqlite import upload_new_data


@dataclass(frozen=True)
class ConvertedPricePLN:
    id: int
    currency: str
    rate: float
    price_in_pln: float
    date: str
    price_in_source_currency: float
    
    

class PriceCurrencyConverterToPLN:
    def __init__(self):
        self.supported_currencies = self.get_currencies()

    def convert_to_pln(self,*, currency: str, price: float) -> ConvertedPricePLN:
        supported_currencies = self.get_currencies()
        if currency not in supported_currencies:
            return "Currency not supported"
        exchange_rate = self.get_exchange_rate_from_api(currency)
        if exchange_rate is None:
            return "Can't fetch the exchange rate"
        converted_amount = round(float(price / exchange_rate), 2)
        data = ConvertedPricePLN(id=None, currency=currency.lower(),
                                price_in_source_currency=converted_amount,
                                rate=exchange_rate,
                                date=datetime.now().strftime("%D:%M:%Y"),
                                price_in_pln=price)
        self.save_data(data)
        return data

    def get_currencies(self):
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/A/")
        if response.status_code == 200:
            supported_currencies = [currency["code"] for currency in response.json()[0]["rates"]]
            return supported_currencies
        else:
            return []

    def get_exchange_rate_from_api(self, currency):
        response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/A/{currency}/?format=json")
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data["rates"][0]["mid"]
            return exchange_rate
        else:
            return None
        
    def get_exchange_rate_from_json(self, json_file):
        pass

    def save_data(self, data):
        if config.ENV == "dev":
            db = JsonFileDatabaseConnector()
            new_data = json.dumps(dataclasses.asdict(data))
            db.add_data(new_data)
        if config.ENV == "prod":
            upload_new_data(new_data)


        
# convert 100 PLN to EURO and save data in local json database
"""
price = 100
currency = "EUR"
result = PriceCurrencyConverterToPLN().convert_to_pln(price=price, currency=currency)

"""


