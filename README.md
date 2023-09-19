main logic -> task/currency_converter.py


example usage:

price = 100
currency = "EUR"
result = PriceCurrencyConverterToPLN().convert_to_pln(price=price, currency=currency)


saves, 

"5": {
        "id": 5,
        "currency": "eur",
        "rate": 4.6458,
        "price_in_pln": 100,
        "date": "09/19/23:49:2023",
        "price_in_source_currency": 21.52
    },

into our database 
