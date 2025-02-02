import responses

import src.external_api


@responses.activate
def test_get_currency_rate() -> None:
    responses.add(
        responses.GET,
        src.external_api.url,
        json={
            "text": """
    {
        "AUD": {
            "ID": "R01010",
            "NumCode": "036",
            "CharCode": "AUD",
            "Nominal": 1,
            "Name": "Австралийский доллар",
            "Value": 60.8872,
            "Previous": 61.0089
        },
        "AZN": {
            "ID": "R01020A",
            "NumCode": "944",
            "CharCode": "AZN",
            "Nominal": 1,
            "Name": "Азербайджанский манат",
            "Value": 57.5357,
            "Previous": 57.6507
        },
        "GBP": {
            "ID": "R01035",
            "NumCode": "826",
            "CharCode": "GBP",
            "Nominal": 1,
            "Name": "Фунт стерлингов",
            "Value": 121.9406,
            "Previous": 121.8609
        },
        "AMD": {
            "ID": "R01060",
            "NumCode": "051",
            "CharCode": "AMD",
            "Nominal": 100,
            "Name": "Армянских драмов",
            "Value": 24.6158,
            "Previous": 24.6296
        },
        "BYN": {
            "ID": "R01090B",
            "NumCode": "933",
            "CharCode": "BYN",
            "Nominal": 1,
            "Name": "Белорусский рубль",
            "Value": 28.7653,
            "Previous": 28.7122
        },
        "BGN": {
            "ID": "R01100",
            "NumCode": "975",
            "CharCode": "BGN",
            "Nominal": 1,
            "Name": "Болгарский лев",
            "Value": 52.0253,
            "Previous": 52.0941
        },
        "BRL": {
            "ID": "R01115",
            "NumCode": "986",
            "CharCode": "BRL",
            "Nominal": 1,
            "Name": "Бразильский реал",
            "Value": 16.5772,
            "Previous": 16.7266
        },
        "HUF": {
            "ID": "R01135",
            "NumCode": "348",
            "CharCode": "HUF",
            "Nominal": 100,
            "Name": "Форинтов",
            "Value": 24.899,
            "Previous": 25.0373
        },
        "VND": {
            "ID": "R01150",
            "NumCode": "704",
            "CharCode": "VND",
            "Nominal": 10000,
            "Name": "Донгов",
            "Value": 40.2099,
            "Previous": 40.2903
        },
        "HKD": {
            "ID": "R01200",
            "NumCode": "344",
            "CharCode": "HKD",
            "Nominal": 1,
            "Name": "Гонконгский доллар",
            "Value": 12.5737,
            "Previous": 12.6021
        },
        "GEL": {
            "ID": "R01210",
            "NumCode": "981",
            "CharCode": "GEL",
            "Nominal": 1,
            "Name": "Лари",
            "Value": 34.0081,
            "Previous": 34.0488
        },
        "DKK": {
            "ID": "R01215",
            "NumCode": "208",
            "CharCode": "DKK",
            "Nominal": 1,
            "Name": "Датская крона",
            "Value": 13.6369,
            "Previous": 13.6529
        },
        "AED": {
            "ID": "R01230",
            "NumCode": "784",
            "CharCode": "AED",
            "Nominal": 1,
            "Name": "Дирхам ОАЭ",
            "Value": 26.6333,
            "Previous": 26.6865
        },
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 97.8107,
            "Previous": 98.0062
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 102.1301,
            "Previous": 102.7782
        },
        "EGP": {
            "ID": "R01240",
            "NumCode": "818",
            "CharCode": "EGP",
            "Nominal": 10,
            "Name": "Египетских фунтов",
            "Value": 19.4691,
            "Previous": 19.5093
        },
        "INR": {
            "ID": "R01270",
            "NumCode": "356",
            "CharCode": "INR",
            "Nominal": 10,
            "Name": "Индийских рупий",
            "Value": 11.2891,
            "Previous": 11.3192
        },
        "IDR": {
            "ID": "R01280",
            "NumCode": "360",
            "CharCode": "IDR",
            "Nominal": 10000,
            "Name": "Рупий",
            "Value": 60.1579,
            "Previous": 60.4977
        },
        "KZT": {
            "ID": "R01335",
            "NumCode": "398",
            "CharCode": "KZT",
            "Nominal": 100,
            "Name": "Тенге",
            "Value": 18.8358,
            "Previous": 18.9622
        },
        "CAD": {
            "ID": "R01350",
            "NumCode": "124",
            "CharCode": "CAD",
            "Nominal": 1,
            "Name": "Канадский доллар",
            "Value": 67.8581,
            "Previous": 67.8948
        },
        "QAR": {
            "ID": "R01355",
            "NumCode": "634",
            "CharCode": "QAR",
            "Nominal": 1,
            "Name": "Катарский риал",
            "Value": 26.8711,
            "Previous": 26.9248
        },
        "KGS": {
            "ID": "R01370",
            "NumCode": "417",
            "CharCode": "KGS",
            "Nominal": 10,
            "Name": "Сомов",
            "Value": 11.1848,
            "Previous": 11.2071
        },
        "CNY": {
            "ID": "R01375",
            "NumCode": "156",
            "CharCode": "CNY",
            "Nominal": 1,
            "Name": "Юань",
            "Value": 13.2638,
            "Previous": 13.3729
        },
        "MDL": {
            "ID": "R01500",
            "NumCode": "498",
            "CharCode": "MDL",
            "Nominal": 10,
            "Name": "Молдавских леев",
            "Value": 52.3713,
            "Previous": 52.5807
        },
        "NZD": {
            "ID": "R01530",
            "NumCode": "554",
            "CharCode": "NZD",
            "Nominal": 1,
            "Name": "Новозеландский доллар",
            "Value": 55.043,
            "Previous": 55.496
        },
        "NOK": {
            "ID": "R01535",
            "NumCode": "578",
            "CharCode": "NOK",
            "Nominal": 10,
            "Name": "Норвежских крон",
            "Value": 86.513,
            "Previous": 86.503
        },
        "PLN": {
            "ID": "R01565",
            "NumCode": "985",
            "CharCode": "PLN",
            "Nominal": 1,
            "Name": "Злотый",
            "Value": 24.1056,
            "Previous": 24.2632
        },
        "RON": {
            "ID": "R01585F",
            "NumCode": "946",
            "CharCode": "RON",
            "Nominal": 1,
            "Name": "Румынский лей",
            "Value": 20.3946,
            "Previous": 20.4824
        },
        "XDR": {
            "ID": "R01589",
            "NumCode": "960",
            "CharCode": "XDR",
            "Nominal": 1,
            "Name": "СДР (специальные права заимствования)",
            "Value": 127.6772,
            "Previous": 127.9157
        },
        "SGD": {
            "ID": "R01625",
            "NumCode": "702",
            "CharCode": "SGD",
            "Nominal": 1,
            "Name": "Сингапурский доллар",
            "Value": 72.1744,
            "Previous": 72.4576
        },
        "TJS": {
            "ID": "R01670",
            "NumCode": "972",
            "CharCode": "TJS",
            "Nominal": 10,
            "Name": "Сомони",
            "Value": 89.5358,
            "Previous": 89.8678
        },
        "THB": {
            "ID": "R01675",
            "NumCode": "764",
            "CharCode": "THB",
            "Nominal": 10,
            "Name": "Батов",
            "Value": 29.0653,
            "Previous": 29.0268
        },
        "TRY": {
            "ID": "R01700J",
            "NumCode": "949",
            "CharCode": "TRY",
            "Nominal": 10,
            "Name": "Турецких лир",
            "Value": 27.3572,
            "Previous": 27.4229
        },
        "TMT": {
            "ID": "R01710A",
            "NumCode": "934",
            "CharCode": "TMT",
            "Nominal": 1,
            "Name": "Новый туркменский манат",
            "Value": 27.9459,
            "Previous": 28.0018
        },
        "UZS": {
            "ID": "R01717",
            "NumCode": "860",
            "CharCode": "UZS",
            "Nominal": 10000,
            "Name": "Узбекских сумов",
            "Value": 75.4886,
            "Previous": 75.5734
        },
        "UAH": {
            "ID": "R01720",
            "NumCode": "980",
            "CharCode": "UAH",
            "Nominal": 10,
            "Name": "Гривен",
            "Value": 23.3861,
            "Previous": 23.3741
        },
        "CZK": {
            "ID": "R01760",
            "NumCode": "203",
            "CharCode": "CZK",
            "Nominal": 10,
            "Name": "Чешских крон",
            "Value": 40.5181,
            "Previous": 40.5403
        },
        "SEK": {
            "ID": "R01770",
            "NumCode": "752",
            "CharCode": "SEK",
            "Nominal": 10,
            "Name": "Шведских крон",
            "Value": 88.7118,
            "Previous": 88.9418
        },
        "CHF": {
            "ID": "R01775",
            "NumCode": "756",
            "CharCode": "CHF",
            "Nominal": 1,
            "Name": "Швейцарский франк",
            "Value": 107.3899,
            "Previous": 107.972
        },
        "RSD": {
            "ID": "R01805F",
            "NumCode": "941",
            "CharCode": "RSD",
            "Nominal": 100,
            "Name": "Сербских динаров",
            "Value": 86.77,
            "Previous": 87.1849
        },
        "ZAR": {
            "ID": "R01810",
            "NumCode": "710",
            "CharCode": "ZAR",
            "Nominal": 10,
            "Name": "Рэндов",
            "Value": 52.6119,
            "Previous": 52.9663
        },
        "KRW": {
            "ID": "R01815",
            "NumCode": "410",
            "CharCode": "KRW",
            "Nominal": 1000,
            "Name": "Вон",
            "Value": 68.2416,
            "Previous": 68.1972
        },
        "JPY": {
            "ID": "R01820",
            "NumCode": "392",
            "CharCode": "JPY",
            "Nominal": 100,
            "Name": "Иен",
            "Value": 63.3776,
            "Previous": 63.332}}"""
        },
        status=200,
    )
    result = src.external_api.get_currency_rate("USD", "RUB")
    assert result == 97.8107


@responses.activate
def test_get_overall_stocks(example_user_stocks_fixture) -> None:
    stocks = example_user_stocks_fixture.get("user_stocks")
    responses.add(
        responses.GET,
        src.external_api.get_stocks_url(stocks),
        json={
            "text": """{"pagination":{"limit":100,"offset":0,"count":5,"total":5},"data":[{"open":247.19,
                  "high":247.19,"low":233.44,"close":236.0,"volume":100959800.0,"adj_high":247.19,"adj_low":233.44,
                  "adj_close":236.0,"adj_open":247.19,"adj_volume":101075128.0,"split_factor":1.0,"dividend":0.0,
                  "symbol":"AAPL","exchange":"XNAS","date":"2025-01-31T00:00:00+0000"},{"open":236.5,"high":240.29,
                  "low":236.41,"close":237.68,"volume":36162377.0,"adj_high":240.29,"adj_low":236.41,
                  "adj_close":237.68,"adj_open":236.5,"adj_volume":36162377.0,"split_factor":1.0,"dividend":0.0,
                  "symbol":"AMZN","exchange":"XNAS","date":"2025-01-31T00:00:00+0000"},{"open":202.0,"high":205.48,
                  "low":201.8,"close":204.02,"volume":32041952.0,"adj_high":205.48,"adj_low":201.8,
                  "adj_close":204.02,"adj_open":202.0,"adj_volume":32041952.0,"split_factor":1.0,"dividend":0.0,
                  "symbol":"GOOGL","exchange":"XNAS","date":"2025-01-31T00:00:00+0000"},{"open":418.98,"high":420.69,
                  "low":414.91,"close":415.06,"volume":34161900.0,"adj_high":420.69,"adj_low":414.91,
                  "adj_close":415.06,"adj_open":418.98,"adj_volume":34223388.0,"split_factor":1.0,"dividend":0.0,
                  "symbol":"MSFT","exchange":"XNAS","date":"2025-01-31T00:00:00+0000"},{"open":401.53,"high":419.99,
                  "low":401.34,"close":404.6,"volume":83568219.0,"adj_high":419.99,"adj_low":401.34,
                  "adj_close":404.6,"adj_open":401.53,"adj_volume":83568219.0,"split_factor":1.0,"dividend":0.0,
                  "symbol":"TSLA","exchange":"XNAS","date":"2025-01-31T00:00:00+0000"}]} """
        },
        status=200,
    )
    result = src.external_api.get_overall_stocks(stocks)
    assert result == [
        {
            "open": 247.19,
            "high": 247.19,
            "low": 233.44,
            "close": 236.0,
            "volume": 100959800.0,
            "adj_high": 247.19,
            "adj_low": 233.44,
            "adj_close": 236.0,
            "adj_open": 247.19,
            "adj_volume": 101075128.0,
            "split_factor": 1.0,
            "dividend": 0.0,
            "symbol": "AAPL",
            "exchange": "XNAS",
            "date": "2025-01-31T00:00:00+0000",
        },
        {
            "open": 236.5,
            "high": 240.29,
            "low": 236.41,
            "close": 237.68,
            "volume": 36162377.0,
            "adj_high": 240.29,
            "adj_low": 236.41,
            "adj_close": 237.68,
            "adj_open": 236.5,
            "adj_volume": 36162377.0,
            "split_factor": 1.0,
            "dividend": 0.0,
            "symbol": "AMZN",
            "exchange": "XNAS",
            "date": "2025-01-31T00:00:00+0000",
        },
        {
            "open": 202.0,
            "high": 205.48,
            "low": 201.8,
            "close": 204.02,
            "volume": 32041952.0,
            "adj_high": 205.48,
            "adj_low": 201.8,
            "adj_close": 204.02,
            "adj_open": 202.0,
            "adj_volume": 32041952.0,
            "split_factor": 1.0,
            "dividend": 0.0,
            "symbol": "GOOGL",
            "exchange": "XNAS",
            "date": "2025-01-31T00:00:00+0000",
        },
        {
            "open": 418.98,
            "high": 420.69,
            "low": 414.91,
            "close": 415.06,
            "volume": 34161900.0,
            "adj_high": 420.69,
            "adj_low": 414.91,
            "adj_close": 415.06,
            "adj_open": 418.98,
            "adj_volume": 34223388.0,
            "split_factor": 1.0,
            "dividend": 0.0,
            "symbol": "MSFT",
            "exchange": "XNAS",
            "date": "2025-01-31T00:00:00+0000",
        },
        {
            "open": 401.53,
            "high": 419.99,
            "low": 401.34,
            "close": 404.6,
            "volume": 83568219.0,
            "adj_high": 419.99,
            "adj_low": 401.34,
            "adj_close": 404.6,
            "adj_open": 401.53,
            "adj_volume": 83568219.0,
            "split_factor": 1.0,
            "dividend": 0.0,
            "symbol": "TSLA",
            "exchange": "XNAS",
            "date": "2025-01-31T00:00:00+0000",
        },
    ]


@responses.activate
def test_get_overall_currencies() -> None:
    responses.add(
        responses.GET,
        src.external_api.url,
        json={
            "text": """
{
    "Date": "2025-02-01T11:30:00+03:00",
    "PreviousDate": "2025-01-31T11:30:00+03:00",
    "Timestamp": "2025-02-02T19:00:00+03:00",
    "Valute": {
        "AUD": {
            "ID": "R01010",
            "NumCode": "036",
            "CharCode": "AUD",
            "Nominal": 1,
            "Name": "Австралийский доллар",
            "Value": 60.8872,
            "Previous": 61.0089
        },
        "AZN": {
            "ID": "R01020A",
            "NumCode": "944",
            "CharCode": "AZN",
            "Nominal": 1,
            "Name": "Азербайджанский манат",
            "Value": 57.5357,
            "Previous": 57.6507
        },
        "GBP": {
            "ID": "R01035",
            "NumCode": "826",
            "CharCode": "GBP",
            "Nominal": 1,
            "Name": "Фунт стерлингов",
            "Value": 121.9406,
            "Previous": 121.8609
        },
        "AMD": {
            "ID": "R01060",
            "NumCode": "051",
            "CharCode": "AMD",
            "Nominal": 100,
            "Name": "Армянских драмов",
            "Value": 24.6158,
            "Previous": 24.6296
        },
        "BYN": {
            "ID": "R01090B",
            "NumCode": "933",
            "CharCode": "BYN",
            "Nominal": 1,
            "Name": "Белорусский рубль",
            "Value": 28.7653,
            "Previous": 28.7122
        },
        "BGN": {
            "ID": "R01100",
            "NumCode": "975",
            "CharCode": "BGN",
            "Nominal": 1,
            "Name": "Болгарский лев",
            "Value": 52.0253,
            "Previous": 52.0941
        },
        "BRL": {
            "ID": "R01115",
            "NumCode": "986",
            "CharCode": "BRL",
            "Nominal": 1,
            "Name": "Бразильский реал",
            "Value": 16.5772,
            "Previous": 16.7266
        },
        "HUF": {
            "ID": "R01135",
            "NumCode": "348",
            "CharCode": "HUF",
            "Nominal": 100,
            "Name": "Форинтов",
            "Value": 24.899,
            "Previous": 25.0373
        },
        "VND": {
            "ID": "R01150",
            "NumCode": "704",
            "CharCode": "VND",
            "Nominal": 10000,
            "Name": "Донгов",
            "Value": 40.2099,
            "Previous": 40.2903
        },
        "HKD": {
            "ID": "R01200",
            "NumCode": "344",
            "CharCode": "HKD",
            "Nominal": 1,
            "Name": "Гонконгский доллар",
            "Value": 12.5737,
            "Previous": 12.6021
        },
        "GEL": {
            "ID": "R01210",
            "NumCode": "981",
            "CharCode": "GEL",
            "Nominal": 1,
            "Name": "Лари",
            "Value": 34.0081,
            "Previous": 34.0488
        },
        "DKK": {
            "ID": "R01215",
            "NumCode": "208",
            "CharCode": "DKK",
            "Nominal": 1,
            "Name": "Датская крона",
            "Value": 13.6369,
            "Previous": 13.6529
        },
        "AED": {
            "ID": "R01230",
            "NumCode": "784",
            "CharCode": "AED",
            "Nominal": 1,
            "Name": "Дирхам ОАЭ",
            "Value": 26.6333,
            "Previous": 26.6865
        },
        "USD": {
            "ID": "R01235",
            "NumCode": "840",
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 97.8107,
            "Previous": 98.0062
        },
        "EUR": {
            "ID": "R01239",
            "NumCode": "978",
            "CharCode": "EUR",
            "Nominal": 1,
            "Name": "Евро",
            "Value": 102.1301,
            "Previous": 102.7782
        },
        "EGP": {
            "ID": "R01240",
            "NumCode": "818",
            "CharCode": "EGP",
            "Nominal": 10,
            "Name": "Египетских фунтов",
            "Value": 19.4691,
            "Previous": 19.5093
        },
        "INR": {
            "ID": "R01270",
            "NumCode": "356",
            "CharCode": "INR",
            "Nominal": 10,
            "Name": "Индийских рупий",
            "Value": 11.2891,
            "Previous": 11.3192
        },
        "IDR": {
            "ID": "R01280",
            "NumCode": "360",
            "CharCode": "IDR",
            "Nominal": 10000,
            "Name": "Рупий",
            "Value": 60.1579,
            "Previous": 60.4977
        },
        "KZT": {
            "ID": "R01335",
            "NumCode": "398",
            "CharCode": "KZT",
            "Nominal": 100,
            "Name": "Тенге",
            "Value": 18.8358,
            "Previous": 18.9622
        },
        "CAD": {
            "ID": "R01350",
            "NumCode": "124",
            "CharCode": "CAD",
            "Nominal": 1,
            "Name": "Канадский доллар",
            "Value": 67.8581,
            "Previous": 67.8948
        },
        "QAR": {
            "ID": "R01355",
            "NumCode": "634",
            "CharCode": "QAR",
            "Nominal": 1,
            "Name": "Катарский риал",
            "Value": 26.8711,
            "Previous": 26.9248
        },
        "KGS": {
            "ID": "R01370",
            "NumCode": "417",
            "CharCode": "KGS",
            "Nominal": 10,
            "Name": "Сомов",
            "Value": 11.1848,
            "Previous": 11.2071
        },
        "CNY": {
            "ID": "R01375",
            "NumCode": "156",
            "CharCode": "CNY",
            "Nominal": 1,
            "Name": "Юань",
            "Value": 13.2638,
            "Previous": 13.3729
        },
        "MDL": {
            "ID": "R01500",
            "NumCode": "498",
            "CharCode": "MDL",
            "Nominal": 10,
            "Name": "Молдавских леев",
            "Value": 52.3713,
            "Previous": 52.5807
        },
        "NZD": {
            "ID": "R01530",
            "NumCode": "554",
            "CharCode": "NZD",
            "Nominal": 1,
            "Name": "Новозеландский доллар",
            "Value": 55.043,
            "Previous": 55.496
        },
        "NOK": {
            "ID": "R01535",
            "NumCode": "578",
            "CharCode": "NOK",
            "Nominal": 10,
            "Name": "Норвежских крон",
            "Value": 86.513,
            "Previous": 86.503
        },
        "PLN": {
            "ID": "R01565",
            "NumCode": "985",
            "CharCode": "PLN",
            "Nominal": 1,
            "Name": "Злотый",
            "Value": 24.1056,
            "Previous": 24.2632
        },
        "RON": {
            "ID": "R01585F",
            "NumCode": "946",
            "CharCode": "RON",
            "Nominal": 1,
            "Name": "Румынский лей",
            "Value": 20.3946,
            "Previous": 20.4824
        },
        "XDR": {
            "ID": "R01589",
            "NumCode": "960",
            "CharCode": "XDR",
            "Nominal": 1,
            "Name": "СДР (специальные права заимствования)",
            "Value": 127.6772,
            "Previous": 127.9157
        },
        "SGD": {
            "ID": "R01625",
            "NumCode": "702",
            "CharCode": "SGD",
            "Nominal": 1,
            "Name": "Сингапурский доллар",
            "Value": 72.1744,
            "Previous": 72.4576
        },
        "TJS": {
            "ID": "R01670",
            "NumCode": "972",
            "CharCode": "TJS",
            "Nominal": 10,
            "Name": "Сомони",
            "Value": 89.5358,
            "Previous": 89.8678
        },
        "THB": {
            "ID": "R01675",
            "NumCode": "764",
            "CharCode": "THB",
            "Nominal": 10,
            "Name": "Батов",
            "Value": 29.0653,
            "Previous": 29.0268
        },
        "TRY": {
            "ID": "R01700J",
            "NumCode": "949",
            "CharCode": "TRY",
            "Nominal": 10,
            "Name": "Турецких лир",
            "Value": 27.3572,
            "Previous": 27.4229
        },
        "TMT": {
            "ID": "R01710A",
            "NumCode": "934",
            "CharCode": "TMT",
            "Nominal": 1,
            "Name": "Новый туркменский манат",
            "Value": 27.9459,
            "Previous": 28.0018
        },
        "UZS": {
            "ID": "R01717",
            "NumCode": "860",
            "CharCode": "UZS",
            "Nominal": 10000,
            "Name": "Узбекских сумов",
            "Value": 75.4886,
            "Previous": 75.5734
        },
        "UAH": {
            "ID": "R01720",
            "NumCode": "980",
            "CharCode": "UAH",
            "Nominal": 10,
            "Name": "Гривен",
            "Value": 23.3861,
            "Previous": 23.3741
        },
        "CZK": {
            "ID": "R01760",
            "NumCode": "203",
            "CharCode": "CZK",
            "Nominal": 10,
            "Name": "Чешских крон",
            "Value": 40.5181,
            "Previous": 40.5403
        },
        "SEK": {
            "ID": "R01770",
            "NumCode": "752",
            "CharCode": "SEK",
            "Nominal": 10,
            "Name": "Шведских крон",
            "Value": 88.7118,
            "Previous": 88.9418
        },
        "CHF": {
            "ID": "R01775",
            "NumCode": "756",
            "CharCode": "CHF",
            "Nominal": 1,
            "Name": "Швейцарский франк",
            "Value": 107.3899,
            "Previous": 107.972
        },
        "RSD": {
            "ID": "R01805F",
            "NumCode": "941",
            "CharCode": "RSD",
            "Nominal": 100,
            "Name": "Сербских динаров",
            "Value": 86.77,
            "Previous": 87.1849
        },
        "ZAR": {
            "ID": "R01810",
            "NumCode": "710",
            "CharCode": "ZAR",
            "Nominal": 10,
            "Name": "Рэндов",
            "Value": 52.6119,
            "Previous": 52.9663
        },
        "KRW": {
            "ID": "R01815",
            "NumCode": "410",
            "CharCode": "KRW",
            "Nominal": 1000,
            "Name": "Вон",
            "Value": 68.2416,
            "Previous": 68.1972
        },
        "JPY": {
            "ID": "R01820",
            "NumCode": "392",
            "CharCode": "JPY",
            "Nominal": 100,
            "Name": "Иен",
            "Value": 63.3776,
            "Previous": 63.332
        }
    }
}"""
        },
        status=200,
    )
    result = src.external_api.get_overall_currencies()
    assert result == {
        "text": '\n{\n    "Date": "2025-02-01T11:30:00+03:00",\n    "PreviousDate": "2025-01-31T11:30:00+03:00",'
        '\n    "Timestamp": "2025-02-02T19:00:00+03:00",\n    "Valute": {\n        "AUD": {\n            '
        '"ID": "R01010",\n            "NumCode": "036",\n            "CharCode": "AUD",\n            '
        '"Nominal": 1,\n            "Name": "Австралийский доллар",\n            "Value": 60.8872,\n          '
        '  "Previous": 61.0089\n        },\n        "AZN": {\n            "ID": "R01020A",\n            '
        '"NumCode": "944",\n            "CharCode": "AZN",\n            "Nominal": 1,\n            "Name": '
        '"Азербайджанский манат",\n            "Value": 57.5357,\n            "Previous": 57.6507\n        },'
        '\n        "GBP": {\n            "ID": "R01035",\n            "NumCode": "826",\n            '
        '"CharCode": "GBP",\n            "Nominal": 1,\n            "Name": "Фунт стерлингов",\n            '
        '"Value": 121.9406,\n            "Previous": 121.8609\n        },\n        "AMD": {\n            '
        '"ID": "R01060",\n            "NumCode": "051",\n            "CharCode": "AMD",\n            '
        '"Nominal": 100,\n            "Name": "Армянских драмов",\n            "Value": 24.6158,\n            '
        '"Previous": 24.6296\n        },\n        "BYN": {\n            "ID": "R01090B",\n            '
        '"NumCode": "933",\n            "CharCode": "BYN",\n            "Nominal": 1,\n            "Name": '
        '"Белорусский рубль",\n            "Value": 28.7653,\n            "Previous": 28.7122\n        },'
        '\n        "BGN": {\n            "ID": "R01100",\n            "NumCode": "975",\n            '
        '"CharCode": "BGN",\n            "Nominal": 1,\n            "Name": "Болгарский лев",\n            '
        '"Value": 52.0253,\n            "Previous": 52.0941\n        },\n        "BRL": {\n            "ID": '
        '"R01115",\n            "NumCode": "986",\n            "CharCode": "BRL",\n            "Nominal": 1,'
        '\n            "Name": "Бразильский реал",\n            "Value": 16.5772,\n            "Previous": '
        '16.7266\n        },\n        "HUF": {\n            "ID": "R01135",\n            "NumCode": "348",'
        '\n            "CharCode": "HUF",\n            "Nominal": 100,\n            "Name": "Форинтов",'
        '\n            "Value": 24.899,\n            "Previous": 25.0373\n        },\n        "VND": {\n      '
        '      "ID": "R01150",\n            "NumCode": "704",\n            "CharCode": "VND",\n            '
        '"Nominal": 10000,\n            "Name": "Донгов",\n            "Value": 40.2099,\n            '
        '"Previous": 40.2903\n        },\n        "HKD": {\n            "ID": "R01200",\n            '
        '"NumCode": "344",\n            "CharCode": "HKD",\n            "Nominal": 1,\n            "Name": '
        '"Гонконгский доллар",\n            "Value": 12.5737,\n            "Previous": 12.6021\n        },'
        '\n        "GEL": {\n            "ID": "R01210",\n            "NumCode": "981",\n            '
        '"CharCode": "GEL",\n            "Nominal": 1,\n            "Name": "Лари",\n            "Value": '
        '34.0081,\n            "Previous": 34.0488\n        },\n        "DKK": {\n            "ID": "R01215",'
        '\n            "NumCode": "208",\n            "CharCode": "DKK",\n            "Nominal": 1,'
        '\n            "Name": "Датская крона",\n            "Value": 13.6369,\n            "Previous": '
        '13.6529\n        },\n        "AED": {\n            "ID": "R01230",\n            "NumCode": "784",'
        '\n            "CharCode": "AED",\n            "Nominal": 1,\n            "Name": "Дирхам ОАЭ",'
        '\n            "Value": 26.6333,\n            "Previous": 26.6865\n        },\n        "USD": {\n     '
        '       "ID": "R01235",\n            "NumCode": "840",\n            "CharCode": "USD",\n            '
        '"Nominal": 1,\n            "Name": "Доллар США",\n            "Value": 97.8107,\n            '
        '"Previous": 98.0062\n        },\n        "EUR": {\n            "ID": "R01239",\n            '
        '"NumCode": "978",\n            "CharCode": "EUR",\n            "Nominal": 1,\n            "Name": '
        '"Евро",\n            "Value": 102.1301,\n            "Previous": 102.7782\n        },'
        '\n        "EGP": {\n            "ID": "R01240",\n            "NumCode": "818",\n            '
        '"CharCode": "EGP",\n            "Nominal": 10,\n            "Name": "Египетских фунтов",\n           '
        ' "Value": 19.4691,\n            "Previous": 19.5093\n        },\n        "INR": {\n            "ID": '
        '"R01270",\n            "NumCode": "356",\n            "CharCode": "INR",\n            "Nominal": 10,'
        '\n            "Name": "Индийских рупий",\n            "Value": 11.2891,\n            "Previous": '
        '11.3192\n        },\n        "IDR": {\n            "ID": "R01280",\n            "NumCode": "360",'
        '\n            "CharCode": "IDR",\n            "Nominal": 10000,\n            "Name": "Рупий",'
        '\n            "Value": 60.1579,\n            "Previous": 60.4977\n        },\n        "KZT": {\n     '
        '       "ID": "R01335",\n            "NumCode": "398",\n            "CharCode": "KZT",\n            '
        '"Nominal": 100,\n            "Name": "Тенге",\n            "Value": 18.8358,\n            '
        '"Previous": 18.9622\n        },\n        "CAD": {\n            "ID": "R01350",\n            '
        '"NumCode": "124",\n            "CharCode": "CAD",\n            "Nominal": 1,\n            "Name": '
        '"Канадский доллар",\n            "Value": 67.8581,\n            "Previous": 67.8948\n        },'
        '\n        "QAR": {\n            "ID": "R01355",\n            "NumCode": "634",\n            '
        '"CharCode": "QAR",\n            "Nominal": 1,\n            "Name": "Катарский риал",\n            '
        '"Value": 26.8711,\n            "Previous": 26.9248\n        },\n        "KGS": {\n            "ID": '
        '"R01370",\n            "NumCode": "417",\n            "CharCode": "KGS",\n            "Nominal": 10,'
        '\n            "Name": "Сомов",\n            "Value": 11.1848,\n            "Previous": 11.2071\n     '
        '   },\n        "CNY": {\n            "ID": "R01375",\n            "NumCode": "156",\n            '
        '"CharCode": "CNY",\n            "Nominal": 1,\n            "Name": "Юань",\n            "Value": '
        '13.2638,\n            "Previous": 13.3729\n        },\n        "MDL": {\n            "ID": "R01500",'
        '\n            "NumCode": "498",\n            "CharCode": "MDL",\n            "Nominal": 10,'
        '\n            "Name": "Молдавских леев",\n            "Value": 52.3713,\n            "Previous": '
        '52.5807\n        },\n        "NZD": {\n            "ID": "R01530",\n            "NumCode": "554",'
        '\n            "CharCode": "NZD",\n            "Nominal": 1,\n            "Name": "Новозеландский '
        'доллар",\n            "Value": 55.043,\n            "Previous": 55.496\n        },\n        "NOK": {'
        '\n            "ID": "R01535",\n            "NumCode": "578",\n            "CharCode": "NOK",'
        '\n            "Nominal": 10,\n            "Name": "Норвежских крон",\n            "Value": 86.513,'
        '\n            "Previous": 86.503\n        },\n        "PLN": {\n            "ID": "R01565",'
        '\n            "NumCode": "985",\n            "CharCode": "PLN",\n            "Nominal": 1,'
        '\n            "Name": "Злотый",\n            "Value": 24.1056,\n            "Previous": 24.2632\n    '
        '    },\n        "RON": {\n            "ID": "R01585F",\n            "NumCode": "946",\n            '
        '"CharCode": "RON",\n            "Nominal": 1,\n            "Name": "Румынский лей",\n            '
        '"Value": 20.3946,\n            "Previous": 20.4824\n        },\n        "XDR": {\n            "ID": '
        '"R01589",\n            "NumCode": "960",\n            "CharCode": "XDR",\n            "Nominal": 1,'
        '\n            "Name": "СДР (специальные права заимствования)",\n            "Value": 127.6772,'
        '\n            "Previous": 127.9157\n        },\n        "SGD": {\n            "ID": "R01625",'
        '\n            "NumCode": "702",\n            "CharCode": "SGD",\n            "Nominal": 1,'
        '\n            "Name": "Сингапурский доллар",\n            "Value": 72.1744,\n            "Previous": '
        '72.4576\n        },\n        "TJS": {\n            "ID": "R01670",\n            "NumCode": "972",'
        '\n            "CharCode": "TJS",\n            "Nominal": 10,\n            "Name": "Сомони",'
        '\n            "Value": 89.5358,\n            "Previous": 89.8678\n        },\n        "THB": {\n     '
        '       "ID": "R01675",\n            "NumCode": "764",\n            "CharCode": "THB",\n            '
        '"Nominal": 10,\n            "Name": "Батов",\n            "Value": 29.0653,\n            "Previous": '
        '29.0268\n        },\n        "TRY": {\n            "ID": "R01700J",\n            "NumCode": "949",'
        '\n            "CharCode": "TRY",\n            "Nominal": 10,\n            "Name": "Турецких лир",'
        '\n            "Value": 27.3572,\n            "Previous": 27.4229\n        },\n        "TMT": {\n     '
        '       "ID": "R01710A",\n            "NumCode": "934",\n            "CharCode": "TMT",\n            '
        '"Nominal": 1,\n            "Name": "Новый туркменский манат",\n            "Value": 27.9459,'
        '\n            "Previous": 28.0018\n        },\n        "UZS": {\n            "ID": "R01717",'
        '\n            "NumCode": "860",\n            "CharCode": "UZS",\n            "Nominal": 10000,'
        '\n            "Name": "Узбекских сумов",\n            "Value": 75.4886,\n            "Previous": '
        '75.5734\n        },\n        "UAH": {\n            "ID": "R01720",\n            "NumCode": "980",'
        '\n            "CharCode": "UAH",\n            "Nominal": 10,\n            "Name": "Гривен",'
        '\n            "Value": 23.3861,\n            "Previous": 23.3741\n        },\n        "CZK": {\n     '
        '       "ID": "R01760",\n            "NumCode": "203",\n            "CharCode": "CZK",\n            '
        '"Nominal": 10,\n            "Name": "Чешских крон",\n            "Value": 40.5181,\n            '
        '"Previous": 40.5403\n        },\n        "SEK": {\n            "ID": "R01770",\n            '
        '"NumCode": "752",\n            "CharCode": "SEK",\n            "Nominal": 10,\n            "Name": '
        '"Шведских крон",\n            "Value": 88.7118,\n            "Previous": 88.9418\n        },'
        '\n        "CHF": {\n            "ID": "R01775",\n            "NumCode": "756",\n            '
        '"CharCode": "CHF",\n            "Nominal": 1,\n            "Name": "Швейцарский франк",\n            '
        '"Value": 107.3899,\n            "Previous": 107.972\n        },\n        "RSD": {\n            "ID": '
        '"R01805F",\n            "NumCode": "941",\n            "CharCode": "RSD",\n            "Nominal": '
        '100,\n            "Name": "Сербских динаров",\n            "Value": 86.77,\n            "Previous": '
        '87.1849\n        },\n        "ZAR": {\n            "ID": "R01810",\n            "NumCode": "710",'
        '\n            "CharCode": "ZAR",\n            "Nominal": 10,\n            "Name": "Рэндов",'
        '\n            "Value": 52.6119,\n            "Previous": 52.9663\n        },\n        "KRW": {\n     '
        '       "ID": "R01815",\n            "NumCode": "410",\n            "CharCode": "KRW",\n            '
        '"Nominal": 1000,\n            "Name": "Вон",\n            "Value": 68.2416,\n            "Previous": '
        '68.1972\n        },\n        "JPY": {\n            "ID": "R01820",\n            "NumCode": "392",'
        '\n            "CharCode": "JPY",\n            "Nominal": 100,\n            "Name": "Иен",\n          '
        '  "Value": 63.3776,\n            "Previous": 63.332\n        }\n    }\n}'
    }


@responses.activate
def test_get_stock_price() -> None:
    responses.add(
        responses.GET,
        src.external_api.get_stocks_url("GOOGL"),
        json={
            "text": """{"pagination":{"limit":100,"offset":0,
    "count":1,"total":1},"data":[{"open":202.0,"high":205.48,"low":201.8, "close":204.02,"volume":32041952.0,
    "adj_high":205.48,"adj_low":201.8,"adj_close":204.02,"adj_open":202.0, "adj_volume":32041952.0,
    "split_factor":1.0,"dividend":0.0,"symbol":"GOOGL","exchange":"XNAS", "date":"2025-01-31T00:00:00+0000"}]}"""
        },
        status=200,
    )
    result = src.external_api.get_stock_price("GOOGL")
    assert result == 204.02
