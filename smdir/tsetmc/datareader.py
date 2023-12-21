import requests
import pandas as pd


from ..metadata_reader import get_metadata, save_metadata, tables
from ..utils import add_received_time

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
    records["lVal18AFC"] = (
        records["lVal18AFC"].str.replace("ي", "ی").str.replace("ك", "ک")
    )
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


def update_ins_code_list(name: str) -> None:
    if name == "ifb":
        symbols = pd.read_parquet(tables.ifb.bond_list)["symbol"].to_list()
    else:
        raise ValueError
    try:
        code_list = get_metadata(name + "_ins_codes")
        code_list = {} if code_list is None else code_list
    except FileNotFoundError:
        code_list = {}
    for symbol in symbols:
        if symbol in code_list:
            continue
        search_df = search(symbol)
        filt = search_df["lVal18AFC"] == symbol
        if filt.sum() == 1:
            code_list[symbol] = search_df.loc[filt, "insCode"].iloc[0]
        elif len(search_df.index):
            code_list[symbol] = search_df.loc[:, "insCode"].iloc[0]
            print(f"Symbol {symbol} not found in TSETMC search results")
            print(f"Nearest case is: {search_df.loc[:, 'lVal18AFC'].iloc[0]}")
        else:
            print(f"Symbol {symbol} not found in TSETMC search results")
    save_metadata(code_list, name + "_ins_codes")


def update_price_from_source(name: str) -> pd.DataFrame:
    code_list = list(get_metadata(name + "_ins_codes").values())

    try:
        old_price_table = pd.read_parquet(tables.tsetmc.price)
    except FileNotFoundError:
        old_price_table = pd.DataFrame()

    table_list = []
    for code in code_list:
        table_list.append(get_price(code))
    new_price_table = pd.concat(table_list, ignore_index=True).pipe(add_received_time)
    price_table = pd.concat([old_price_table, new_price_table]).drop_duplicates(
        subset=["insCode", "dEven"],
        keep="first",
    )
    price_table.to_parquet(tables.tsetmc.price, index=False)
