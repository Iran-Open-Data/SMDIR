import requests
import pandas as pd


API_URL = "http://cdn.tsetmc.com/api"
HEADERS = {
    "Connection": "keep-alive",
    "Host": "cdn.tsetmc.com",
    "Origin": "http://www.tsetmc.com",
    "Referer": "http://www.tsetmc.com/",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ),
}


def _get_url(url: str):
    response = requests.get(url, headers=HEADERS, timeout=100)
    return response


def search(text: str) -> pd.DataFrame:
    url = f"{API_URL}/Instrument/GetInstrumentSearch/{text}"
    response = _get_url(url)
    records = response.json()["instrumentSearch"]
    records = pd.DataFrame(records)
    return records


def get_price(ins_code) -> pd.DataFrame:
    url = f"{API_URL}/ClosingPrice/GetClosingPriceDailyList/{ins_code}/0"
    response = _get_url(url)
    records = response.json()["closingPriceDaily"]
    result_table = pd.DataFrame.from_records(records)
    return result_table


def get_shareholders(ins_code, date_code) -> pd.DataFrame:
    url = f"http://cdn.tsetmc.com/api/Shareholder/{ins_code}/{date_code}"
    response = _get_url(url)
    shareholders_json = response.json()
    records = shareholders_json["shareShareholder"]
    result_table = pd.DataFrame.from_records(records)
    result_table["insCode"] = ins_code
    return result_table
