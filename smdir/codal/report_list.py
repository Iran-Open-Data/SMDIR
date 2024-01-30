from ..metadata_reader import Table, Column
from .common import codal_directory, CodalReader


# {
#     'Total': 297,
#     'Page': 15,
#     'Letters': [
#         {
#             'SuperVision': {
#                 'UnderSupervision': 0,
#                 'AdditionalInfo': '',
#                 'Reasons': []
#             },
#             'TracingNo': 1148116,
#             'Symbol': 'زرین سهام',
#             'CompanyName': 'صندوق سرمایه گذاری زرین پارسیان',
#             'UnderSupervision': 0,
#             'Title': 'صورت وضعیت پورتفوی صندوق سرمایه گذاری دوره ۱ ماهه منتهی به  ۱۴۰۲/۱۰/۳۰',
#             'LetterCode': '',
#             'SentDateTime': '۱۴۰۲/۱۱/۰۸ ۱۰:۵۴:۲۹',
#             'PublishDateTime': '۱۴۰۲/۱۱/۰۸ ۱۰:۵۴:۲۹',
#             'HasHtml': False,
#             'IsEstimate': False,
#             'Url': '/Reports/Attachment.aspx?LetterSerial=mu8OiX9fcouupVKpVUUUQA%3d%3d',
#             'HasExcel': False,
#             'HasPdf': False,
#             'HasXbrl': False,
#             'HasAttachment': True,
#             'AttachmentUrl': '/Reports/Attachment.aspx?LetterSerial=mu8OiX9fcouupVKpVUUUQA%3d%3d',
#             'PdfUrl': '',
#             'ExcelUrl': '',
#             'XbrlUrl': '',
#             'TedanUrl': 'http://www.tedan.ir'
#         },
#     ]
# }


class TableMetadata(Table):
    directory = codal_directory
    name = "report_list"
    api_params = ["date", "page_number"]
    records_address = ["Letters"]

    Report_ID = Column("TracingNo")
    Symbol = Column("Symbol")
    Name = Column("CompanyName")
    Title = Column("Title")
    Letter_Code = Column("LetterCode")
    Sent_Date = Column("SentDateTime")
    Publication_Date = Column("PublishDateTime")
    Is_Estimate = Column("IsEstimate")
    Has_Html = Column("HasHtml")
    Has_Excel = Column("HasExcel")
    Has_PDF = Column("HasPdf")
    Has_Xbrl = Column("HasXbrl")
    Has_Attachment = Column("HasAttachment")
    URL = Column("Url")
    Attachment_URL = Column("AttachmentUrl")
    PDF_URL = Column("PdfUrl")
    Excel_URL = Column("ExcelUrl")
    Xbrl_URL = Column("XbrlUrl")
    Tedan_URL = Column("TedanUrl")


table_metadata = TableMetadata()

reader = CodalReader(
    url_pattern=(
        "https://search.codal.ir/api/search/v2/q?"
        "FromDate={date}&"
        "ToDate={date}&"
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
