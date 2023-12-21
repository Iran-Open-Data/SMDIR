import pandas as pd

from ..metadata_reader import tables
from ..utils import add_received_time, is_file_up_to_date, download_file
from .scraper import ListScraper, PageScraper, extract_page_data


def get_bond_list() -> pd.DataFrame:
    urls = [
        "https://ifb.ir/MFI/FinancialInstrument.aspx",
        "https://ifb.ir/MFI/qualifiedMFI.aspx",
    ]
    bond_list = pd.concat(
        [ListScraper(url).extract_table() for url in urls], ignore_index=True
    )
    bond_list = bond_list.pipe(add_received_time).sort_values(
        "publication_date", ascending=False
    )
    return bond_list


def update_bond_list_from_source() -> None:
    new_bond_list = get_bond_list()
    try:
        bond_list = (
            pd.concat(
                [pd.read_parquet(tables.ifb.bond_list), new_bond_list],
                ignore_index=True,
            )
            .drop_duplicates(
                subset=["record_id", "document_id", "symbol"],
                keep="first",
            )
            .sort_values("publication_date", ascending=False)
        )
    except FileNotFoundError:
        bond_list = new_bond_list
    bond_list.to_parquet(tables.ifb.bond_list, index=False)


def get_bond_page(record_id: int) -> tuple[int, str, dict[str, list]]:
    scraper = PageScraper(record_id)
    bond_page = scraper.create_record()
    return bond_page


def extract_data_from_pages() -> tuple[pd.DataFrame, pd.DataFrame]:
    bond_page = pd.read_parquet(tables.ifb.bond_page)
    payment_dict = {}
    info_dict = {}

    for _, row in bond_page.iterrows():
        if row["payment_table"]["date"] is None:
            pass
        else:
            payment_dict[row["record_id"]] = pd.DataFrame(row["payment_table"])
        info_dict[row["record_id"]] = extract_page_data(row["page"])

    payment_table = (
        pd.concat(payment_dict, names=["record_id", "index"])
        .reset_index()
        .drop(columns="index")
    )
    info_table = (
        pd.concat(info_dict, names=["record_id", "index"])
        .reset_index()
        .drop(columns="index")
    )
    return payment_table, info_table


def update_bond_page(from_source=False) -> None:
    if from_source:
        update_bond_list_from_source()
        update_bond_page_from_source()
    else:
        download_bond_page()


def update_bond_page_from_source() -> None:
    bond_list = pd.read_parquet(tables.ifb.bond_list, columns=["record_id"])

    try:
        bond_page = pd.read_parquet(tables.ifb.bond_page)
    except FileNotFoundError:
        bond_page = pd.DataFrame()

    if bond_page.empty:
        missing_records = bond_list["record_id"].to_list()
    else:
        filt = -bond_list["record_id"].isin(bond_page["record_id"])
        missing_records = bond_list.loc[filt, "record_id"].to_list()

    page_list = []
    for record_id in missing_records:
        page_list.append(get_bond_page(record_id))

    new_pages = pd.DataFrame(page_list, columns=["record_id", "page", "payment_table"])
    new_pages = add_received_time(new_pages)

    bond_page = pd.concat([bond_page, new_pages], ignore_index=True)
    bond_page.to_parquet(tables.ifb.bond_page, index=False)

    payment_table, info_table = extract_data_from_pages()
    payment_table.to_parquet(tables.ifb.payment_table, index=False)
    info_table.to_parquet(tables.ifb.bond_info, index=False)


def download_bond_page() -> None:
    for file in [tables.ifb.bond_page, tables.ifb.payment_table, tables.ifb.bond_info]:
        if is_file_up_to_date(file):
            continue
        download_file(file)
