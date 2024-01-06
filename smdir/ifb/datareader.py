import pandas as pd

from ..metadata_reader import lib_settings, Table, Column
from ..utils import add_received_time
from .scraper import ListScraper, PageScraper, extract_page_data


ifb_directory = lib_settings.data_dir.joinpath("ifb")

class ListMetadata(Table):
    directory = ifb_directory
    name = "bond_list"

    Row = Column()
    Symbol = Column()
    Publication_Volume = Column()
    Acceptance_Volume = Column()
    Nominal_Amount_per_Note = Column()
    Nominal_Interest_Rate = Column()
    Publication_Date = Column()
    Market_Maker_Name = Column()
    Market_Making_Method = Column()
    Fluctuation_Range = Column()
    Description = Column()
    Documents_and_Records = Column()

bond_list_metadata = ListMetadata()


class InfoMetadata(Table):
    directory = ifb_directory
    name = "bond_info"
    keys = ["ISIN"]

    Company_name_FA = Column()
    Symbol_FA = Column()
    Company_Name = Column()
    Symbol = Column()
    ISIN = Column()
    Market = Column()
    Industry = Column()
    Industry_Subgroup = Column()
    Name = Column()
    Nominal_Value_per_Share = Column()
    Total_Value_of_Securities = Column()
    Accepted_Amount = Column()
    Publication_Date = Column()
    Duration = Column()
    Subject = Column()
    Type = Column()
    Nominal_Interest_Rate = Column()
    Total_Number_of_Securities = Column()
    Number_of_Accepted_Securities = Column()
    Maturity_Date = Column()
    First_Dividend_Payment_Date = Column()
    Dividend_payment_dates = Column()
    Total_Number_of_Delay_Instances_in_Previous_Payments = Column()
    Total_Number_of_Days_Delayed_for_Previous_Payments = Column()
    Issuer = Column()
    Commitment_to_Underwrite = Column()
    Guarantor = Column()
    Trustee = Column()
    Dividend_Payment_Agent = Column()
    Sponsor = Column()
    Market_Maker = Column()
    Selling_Agent = Column()
    Auditor = Column()


bond_info_metadata = InfoMetadata()


class PageMetadata(Table):
    directory = ifb_directory
    name = "bond_page"


bond_page_metadata = PageMetadata()


class PaymentMetadata(Table):
    directory = ifb_directory
    name = "payment_table"


payment_table_metadata = PaymentMetadata()


def update() -> None:
    update_bond_list_from_source()
    update_bond_page_from_source()


def get_bond_list() -> pd.DataFrame:
    urls = [
        "https://ifb.ir/MFI/FinancialInstrument.aspx",
        "https://ifb.ir/MFI/qualifiedMFI.aspx",
    ]
    bond_list = pd.concat(
        [ListScraper(url).extract_table() for url in urls], ignore_index=True
    )
    bond_list = bond_list.pipe(add_received_time).sort_values(
        "Publication_Date", ascending=False
    )
    return bond_list


def update_bond_list_from_source() -> None:
    new_bond_list = get_bond_list()
    try:
        bond_list = (
            pd.concat(
                [pd.read_parquet(bond_list_metadata), new_bond_list],
                ignore_index=True,
            )
            .drop_duplicates(
                subset=["Record_ID"],
                keep="first",
            )
            .sort_values("Publication_Date", ascending=False)
        )
    except FileNotFoundError:
        bond_list = new_bond_list
    bond_list.to_parquet(bond_list_metadata, index=False)


def get_bond_page(record_id: int) -> tuple[int, str, dict[str, list]]:
    scraper = PageScraper(record_id)
    bond_page = scraper.create_record()
    return bond_page


def extract_data_from_pages() -> tuple[pd.DataFrame, pd.DataFrame]:
    bond_page = (
        pd.read_parquet(bond_page_metadata)
        .sort_values("received_time", ascending=False)
        .drop_duplicates("Record_ID", keep="first")
    )
    payment_dict = {}
    info_dict = {}

    for _, row in bond_page.iterrows():
        if row["payment_table"]["date"] is None:
            pass
        else:
            payment_dict[row["Record_ID"]] = pd.DataFrame(row["payment_table"])
        info_dict[row["Record_ID"]] = extract_page_data(row["page"])

    payment_table = (
        pd.concat(payment_dict, names=["Record_ID", "index"])
        .reset_index()
        .drop(columns="index")
    )
    payment_table["value"] = (
        payment_table["value"].str.replace("/", ".").str.replace(",", "").astype(float)
    )
    info_table = (
        pd.concat(info_dict, names=["Record_ID", "index"])
        .reset_index()
        .drop(columns="index")
    )
    return payment_table, info_table


def update_bond_page_from_source() -> None:
    bond_list = pd.read_parquet(bond_list_metadata, columns=["Record_ID"])

    try:
        bond_page = pd.read_parquet(bond_page_metadata)
    except FileNotFoundError:
        bond_page = pd.DataFrame()

    if bond_page.empty:
        missing_records = bond_list["Record_ID"].to_list()
    else:
        filt = -bond_list["Record_ID"].isin(bond_page["Record_ID"])
        missing_records = bond_list.loc[filt, "Record_ID"].to_list()

    page_list = []
    for record_id in missing_records:
        page_list.append(get_bond_page(record_id))

    new_pages = pd.DataFrame(page_list, columns=["Record_ID", "page", "payment_table"])
    new_pages = add_received_time(new_pages)

    bond_page = pd.concat([bond_page, new_pages], ignore_index=True)
    bond_page.to_parquet(bond_page_metadata, index=False)

    payment_table, info_table = extract_data_from_pages()
    info_table.to_parquet(bond_info_metadata, index=False)
    payment_table.to_parquet(payment_table_metadata, index=False)
