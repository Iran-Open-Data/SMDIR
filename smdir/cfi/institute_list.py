from .common import CFIReader, cfi_directory
from ..metadata_reader import Table, Column


# {
#     "data": [
#         {
#             "InstituteTypeId": 1,
#             "InstituteType": "پردازش اطلاعات مالی",
#             "InstituteKindId": 3,
#             "InstituteKind": "سهامی خاص",
#             "SEORegisterNo": 12175,
#             "Website": "https://enigma.ir/",
#             "Name": "پردازش اطلاعات مالی آرتا",
#             "NationalId": "14008252855",
#             "CEO": "سعید محمدخانی نژاد",
#             "CEOMobileNo": null,
#             "StateId": null,
#             "State": null,
#             "Id": 4107
#         },
#     ],
#     "total": 1069
# }


class TableMetadata(Table):
    directory = cfi_directory
    name = "institute_list"
    records_address = ["data"]

    CFI_ID = Column("Id")
    SEO_ID = Column("SEORegisterNo")
    Name = Column("Name")
    Institute_Type = Column("InstituteType")
    Institute_Kind = Column("InstituteKind")
    Website = Column("Website")
    National_ID = Column("NationalId")
    CEO = Column("CEO")
    CEOMobileNo = Column("CEOMobileNo")
    State = Column("State")


table_metadata = TableMetadata()


reader = CFIReader(
    url_pattern = "https://cfi.rbcapi.ir/institutes?offset=0&limit=10000&lng=fa",
    table_metadata=table_metadata,
)
