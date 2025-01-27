import os.path

import requests
from dotenv import load_dotenv
import json

load_dotenv()


def get_currency_rate(from_currency: str, to_currency: str) -> float:
    api_key = os.getenv("API_KEY")
    url = f"https://exchange-rates.abstractapi.com/v1/live/?api_key={api_key}&base={from_currency}&target={to_currency}"
    response = requests.get(url)
    # "https://exchange-rates.abstractapi.com/v1/live/?api_key=1cb8cc523f0c4aa7a5bacbb96a4be599&base=USD&target=EUR")
    if response.ok:
        content = json.loads(response.text)
        rate = content.get("exchange_rates")
        if rate:
            return rate.get("RUB", 0.0)
        else:
            return 0.0
    else:
        return 0.0


if __name__ == '__main__':
    """
    headers = {"apikey": api_key}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
    response = requests.get(url, headers=headers)

    if response.ok:
    from_currency = 'USD'
    to_currency = 'RUB'
    """
