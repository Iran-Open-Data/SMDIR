from ..metadata_reader import Table, Column
from .common import codal_directory, CodalReader


class TableMetadata(Table):
    directory = codal_directory
    name = "publisher_report_list"
    api_params = ["symbol", "page_number"]
    records_address = ["Letters"]

    Symbol = Column("Symbol")
    Name = Column("CompanyName")


table_metadata = TableMetadata()

reader = CodalReader(
    url_pattern=(
        "https://search.codal.ir/api/search/v2/q?"
        "Symbol={symbol}&"
        "PageNumber={page_number}&"
        "Audited=true&"
        "AuditorRef=-1&"
        "Category=-1&"
        "Childs=true&"
        "CompanyState=-1&"
        "CompanyType=-1&"
        "Consolidatable=true&"
        "IsNotAudited=false&"
        "Length=-1&"
        "LetterType=-1&"
        "Mains=true&"
        "NotAudited=true&"
        "NotConsolidatable=true&"
        "Publisher=false&"
        "TracingNo=-1&"
        "search=true"
    ),
    table_metadata=table_metadata,
)
