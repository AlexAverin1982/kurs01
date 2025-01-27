import os.path

import requests
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    api_key = os.getenv("API_KEY")
    """
    headers = {"apikey": api_key}
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={convert_to}&from={convert_from}&amount={amount}"
    response = requests.get(url, headers=headers)

    if response.ok:
    """
    from_currency = 'USD'
    to_currency = 'RUB'
    url = f"https://exchange-rates.abstractapi.com/v1/live/?api_key={api_key}&base={from_currency}&target={to_currency}"

    response = requests.get(url)
    # "https://exchange-rates.abstractapi.com/v1/live/?api_key=1cb8cc523f0c4aa7a5bacbb96a4be599&base=USD&target=EUR")
    print(response.status_code)
    print(response.content)
