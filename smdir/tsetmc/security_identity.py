import pandas as pd
from pydantic import BaseModel, ConfigDict

from .common import TSETMCReader, tsetmc_directory
from ..metadata_reader import Table, Column
from ..lib_types import Int


# Response Sample:
# {
#   'instrumentIdentity': {
#       'sector': {
#           'dEven': 0,
#           'cSecVal': '27 ',
#           'lSecVal': 'فلزات اساسي'
#       },
#       'subSector': {
#           'dEven': 0,
#           'cSecVal': None,
#           'cSoSecVal': 2710,
#           'lSoSecVal': 'توليد آهن و فولاد پايه'
#       },
#       'cValMne': 'FOLD1',
#       'lVal18': 'S*Mobarakeh Steel',
#       'cSocCSAC': 'FOLD',
#       'lSoc30': 'فولاد مباركه اصفهان',
#       'yMarNSC': 'NO',
#       'yVal': '300',
#       'insCode': '0',
#       'lVal30': 'فولاد مباركه اصفهان',
#       'lVal18AFC': 'فولاد',
#       'flow': 0,
#       'cIsin': 'IRO1FOLD0009',
#       'zTitad': 0.0,
#       'baseVol': 0,
#       'instrumentID': 'IRO1FOLD0001',
#       'cgrValCot': 'N1',
#       'cComVal': '1',
#       'lastDate': 0,
#       'sourceID': 0,
#       'flowTitle': '',
#       'cgrValCotTitle': 'بازار اول (تابلوی اصلی) بورس'
#   }
# }


class _Sector(BaseModel):
    dEven: int
    cSecVal: Int
    lSecVal: str


class _SubSector(BaseModel):
    dEven: int
    cSecVal: str | None
    cSoSecVal: int
    lSoSecVal: str


class _InstrumentIdentity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sector: _Sector
    subSector: _SubSector

    cValMne: str
    lVal18: str
    cSocCSAC: str
    lSoc30: str
    yMarNSC: str
    yVal: str
    insCode: str
    lVal30: str
    lVal18AFC: str
    flow: int
    cIsin: str
    zTitad: float
    baseVol: int
    instrumentID: str
    cgrValCot: str
    cComVal: str
    lastDate: int
    sourceID: int
    flowTitle: str
    cgrValCotTitle: str


class Validator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    instrumentIdentity: _InstrumentIdentity


class TableMetadata(Table):
    directory = tsetmc_directory
    name = "security_identity"
    api_params = ["ins_code"]
    records_address = ["instrumentIdentity"]
    keys = ["INS_Code"]
    validator = Validator

    INS_Code = Column()
    ISIN = Column("instrumentID")
    Company_ISIN = Column("cIsin")
    Symbol = Column("cValMne")
    Short_Symbol = Column("cSocCSAC")
    Name = Column("lVal18")
    Farsi_Symbol = Column("lVal18AFC")
    Farsi_Name = Column("lSoc30")
    Market_Code = Column("cComVal")
    Market_Title = Column("cgrValCotTitle")
    Sector_Code = Column(("sector", "cSecVal"))
    Sector_Title = Column(("sector", "lSecVal"))
    Sub_Sector_Code = Column(("subSector", "cSoSecVal"))
    Sub_Sector_Title = Column(("subSector", "lSoSecVal"))

    def post_process(self, table: pd.DataFrame) -> pd.DataFrame:
        table = table.rename(columns={"ins_code": "INS_Code"})
        return table


table_metadata = TableMetadata()


reader = TSETMCReader(
    url_pattern="https://cdn.tsetmc.com/api/Instrument/GetInstrumentIdentity/{ins_code}",
    table_metadata=table_metadata,
)
