from pandas import DataFrame
from pydantic import BaseModel, ConfigDict

from .common import TSETMCReader, tsetmc_directory
from ..metadata_reader import Table, Column

# {
#     "shareShareholder": [
#         {
#             "shareHolderID": 7899,
#             "shareHolderName": "شركت تدبيرسرمايه آراد-سهامي خاص-",
#             "cIsin": "IRO1IKCO0008",
#             "dEven": 20240106,
#             "numberOfShares": 45249410200.0,
#             "perOfShares": 15.000,
#             "change": 1,
#             "changeAmount": 0.0,
#             "shareHolderShareID": 0
#         },
#         {
#             "shareHolderID": 650,
#             "shareHolderName": "شركت گسترش سرمايه گذاري ايران خودرو-سهامي عام-",
#             "cIsin": "IRO1IKCO0008",
#             "dEven": 20240106,
#             "numberOfShares": 32797202579.0,
#             "perOfShares": 10.870,
#             "change": 1,
#             "changeAmount": 0.0,
#             "shareHolderShareID": 0
#         },
# }


class _Shareholder(BaseModel):
    shareHolderID: int
    shareHolderName: str
    cIsin: str
    dEven: int
    numberOfShares: float
    perOfShares: float
    change: int
    changeAmount: float
    shareHolderShareID: int


class Validator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    shareShareholder: list[_Shareholder]


class TableMetadata(Table):
    directory = tsetmc_directory
    name = "shareholders"
    api_params = ["ins_code", "date_id"]
    records_address = ["shareShareholder"]
    keys = ["INS_Code", "Date_ID", "Shareholder_ID"]
    validator = Validator
    # partition = ["ins_code"]

    INS_Code = Column()
    Date_ID = Column("dEven")
    Shareholder_ID = Column("shareHolderID")
    Shareholder_Name = Column("shareHolderName")
    Shareholder_ISIN = Column("cIsin")
    Number_of_Shares = Column("numberOfShares")
    Share_Percentage = Column("perOfShares")

    def post_process(self, table: DataFrame) -> DataFrame:
        return (
            table.sort_values(["date_id", "Date_ID"], ascending=False)
            .drop_duplicates(["ins_code", "date_id", "Shareholder_ID"], keep="first")
            .drop(columns=["Date_ID"])
            .rename(columns={"ins_code": "INS_Code", "date_id": "Date_ID"})
        )


table_metadata = TableMetadata()

reader = TSETMCReader(
    url_pattern="https://cdn.tsetmc.com/api/Shareholder/{ins_code}/{date_id}",
    table_metadata=table_metadata,
)
