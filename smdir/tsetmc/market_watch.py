from .common import TSETMCReader, tsetmc_directory
from ..metadata_reader import Table, Column


class TableMetadata(Table):
    directory = tsetmc_directory
    name = "market_watch"
    records_address = ["marketwatch"]

    Symbol = Column("lva")
    Name = Column("lvc")
    EPS = Column("eps")
    INS_Code = Column("insCode")


table_metadata = TableMetadata()


reader = TSETMCReader(
    url_pattern=(
        "https://cdn.tsetmc.com/api/ClosingPrice/GetMarketWatch?"
        "market=0&"
        "paperTypes[0]=1&"
        "paperTypes[1]=2&"
        "paperTypes[2]=3&"
        "paperTypes[3]=4&"
        "paperTypes[4]=5&"
        "paperTypes[5]=6&"
        "paperTypes[6]=7&"
        "paperTypes[7]=8&"
        "paperTypes[8]=9&"
        "showTraded=false&"
        "withBestLimits=true"
    ),
    table_metadata=table_metadata,
)
