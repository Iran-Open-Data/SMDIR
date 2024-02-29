import pandas as pd
from pydantic import BaseModel, ConfigDict

from .common import TSETMCReader, tsetmc_directory
from ..metadata_reader import Table, Column


# {
#     "closingPriceDaily": [
#         {
#             "priceChange": 0.00,
#             "priceMin": 0.00,
#             "priceMax": 0.00,
#             "priceYesterday": 960000.00,
#             "priceFirst": 0.00,
#             "last": false,
#             "id": 0,
#             "insCode": "16374922288786629",
#             "dEven": 20240101,
#             "hEven": 61140,
#             "pClosing": 960000.00,
#             "iClose": false,
#             "yClose": true,
#             "pDrCotVal": 960000.00,
#             "zTotTran": 0.0,
#             "qTotTran5J": 0.0,
#             "qTotCap": 0.00
#         },
#         {
#             "priceChange": 0.00,
#             "priceMin": 0.00,
#             "priceMax": 0.00,
#             "priceYesterday": 960000.00,
#             "priceFirst": 0.00,
#             "last": false,
#             "id": 0,
#             "insCode": "16374922288786629",
#             "dEven": 20231231,
#             "hEven": 61142,
#             "pClosing": 960000.00,
#             "iClose": false,
#             "yClose": true,
#             "pDrCotVal": 960000.00,
#             "zTotTran": 0.0,
#             "qTotTran5J": 0.0,
#             "qTotCap": 0.00
#         },
#     ]
# }


class _PriceRecord(BaseModel):
    priceChange: float
    priceMin: float
    priceMax: float
    priceYesterday: float
    priceFirst: float
    last: float
    insCode: str
    dEven: int
    hEven: int
    pClosing: float
    iClose: bool
    yClose: bool
    pDrCotVal: float
    zTotTran: float
    qTotTran5J: float
    qTotCap: float


class Validator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    closingPriceDaily: list[_PriceRecord]


class TableMetadata(Table):
    directory = tsetmc_directory
    name = "daily_closing_price"
    api_params = ["ins_code"]
    records_address = ["closingPriceDaily"]
    validator = Validator
    keys = ["INS_Code", "Date_ID"]

    INS_Code = Column("insCode")
    Date_ID = Column("dEven")
    Yesterday_Price = Column("priceYesterday")
    Closing_Price = Column("pClosing")
    Price_Change = Column("priceChange")
    First_Price = Column("priceFirst")
    Minimum_Price = Column("priceMin")
    Maximum_Price = Column("priceMax")
    Number_of_Transactions = Column("zTotTran")
    Volume_of_Transactions = Column("qTotTran5J")
    Value_of_Transactions = Column("qTotCap")

    def post_process(self, table: pd.DataFrame) -> pd.DataFrame:
        return (
            table
            .loc[lambda df: df["Number_of_Transactions"].gt(0)]
            .drop(columns=["ins_code", "recived_time"])
            .assign(Date=lambda df: pd.to_datetime(df["Date_ID"], format=r"%Y%m%d"))
        )


table_metadata = TableMetadata()

reader = TSETMCReader(
    url_pattern="https://cdn.tsetmc.com/api/ClosingPrice/GetClosingPriceDailyList/{ins_code}/0",
    table_metadata=table_metadata,
)
