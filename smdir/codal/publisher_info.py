from bs4 import BeautifulSoup
import pandas as pd

from ..metadata_reader import Table, Column
from .common import codal_directory, CodalReader


page_titles = {
    13: "Symbol",
    14: "Symbol_en",
    11: "Name",
    16: "Name_en",
    21: "Registered_Capital",
    23: "Unregistered_Capital",
    31: "ISIC",
    41: "ISIN",
    43: "National_ID",
    51: "Status",
    56: "Status_en",
    53: "Year_End",
    61: "Reporting_Type",
    62: "Reporting_Type_en",
    67: "Object",
    68: "Object_en",
    75: "Factory_Address",
    76: "Factory_Address_en",
    81: "Factory_Phone",
    87: "Factory_Fax",
    93: "Stock_Affairs_Office_Address",
    94: "Stock_Affairs_Office_Address_en",
    99: "Stock_Affairs_Office_Phone",
    105: "Stock_Affairs_Office_Fax",
    111: "Centeral_Office_Address",
    112: "Centeral_Office_Address_en",
    117: "Centeral_Office_Phone",
    123: "Centeral_Office_Fax",
    129: "Managing_Director",
    130: "Managing_Director_en",
    135: "Finantial_Manager",
    136: "Finantial_Manager_en",
    141: "Board_of_Directors",
    142: "Board_of_Directors_en",
    147: "Auditor_and_Legal_Inspector",
    152: "Auditor_and_Legal_Inspector_en",
    149: "Altarnative_Inspector",
    150: "Altarnative_Inspector_en",
    157: "Website",
    158: "Email",
    161: "Fax",
    162: "Phone",
}


def extract_info(html: str) -> pd.Series:
    soup = BeautifulSoup(html, "html.parser")
    items = (
        pd.Series(soup.find_all("td"))
        .apply(lambda x: x.text)
        .str.replace("\n", " ", regex=False)
        .str.strip()
        .replace("", None)
        .loc[list(page_titles.keys())]
    )
    items.index = items.index.map(page_titles)
    items[items.index[-4:]] = (
        items[items.index[-4:]]
        .str.split(" :", expand=True)[1]
        .str.replace(r"\s*", "", regex=True)
        .replace("", None)
    )
    return items


class TableMetadata(Table):
    directory = codal_directory
    name = "publisher_info"
    api_params = ["symbol"]
    is_raw_text = True

    Text = Column("text")

    def post_process(self, table: pd.DataFrame) -> pd.DataFrame:
        return table.loc[:, "Text"].apply(extract_info)


table_metadata = TableMetadata()

reader = CodalReader(
    url_pattern="https://www.codal.ir/Company.aspx?Symbol={symbol}",
    table_metadata=table_metadata,
)
