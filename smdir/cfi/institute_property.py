from .common import CFIReader, cfi_directory
from ..metadata_reader import Table, Column


# {
#     "InstituteTypeId": 1,
#     "InstituteType": "پردازش اطلاعات مالی",
#     "InstituteKindId": 3,
#     "InstituteKind": "سهامی خاص",
#     "LanguageId": 1,
#     "Name": "پردازش اطلاعات مالی آرتا",
#     "RegisterPlaceId": null,
#     "RegisterPlace": null,
#     "SEORegisterNo": 12175,
#     "SEORegisterDate": "1402/06/04",
#     "NationalId": "14008252855",
#     "RegisterNo": "539622",
#     "RegisterDate": "1398/01/18",
#     "ProvinceId": null,
#     "Province": null,
#     "CityId": null,
#     "City": null,
#     "ExpireDate": null,
#     "PostalCode": null,
#     "Email": null,
#     "Website": "https://enigma.ir/",
#     "ListedCapital": 60000,
#     "Status": true,
#     "CEO": "سعید محمدخانی نژاد",
#     "CEOMobileNo": null,
#     "Address": null,
#     "Phone": null,
#     "ActivitySubject": null,
#     "StateId": null,
#     "State": null,
#     "Id": 4107
# }

class TableMetadata(Table):
    directory = cfi_directory
    name = "institute_property"
    api_params = ["id"]

    Institute_Type = Column("InstituteType")
    Institute_Kind = Column("InstituteKind")
    Name = Column("Name")
    Register_Place = Column("RegisterPlace")
    SEO_Register_No = Column("SEORegisterNo")
    SEO_Register_Date = Column("SEORegisterDate")
    National_ID = Column("NationalId")
    Register_No = Column("RegisterNo")
    Register_Date = Column("RegisterDate")
    Province = Column("Province")
    City = Column("City")
    Expire_Date = Column("ExpireDate")
    Postal_Code = Column("PostalCode")
    Email = Column("Email")
    Website = Column("Website")
    Listed_Capital = Column("ListedCapital")
    Status = Column("Status")
    CEO = Column("CEO")
    CEO_Mobile_No = Column("CEOMobileNo")
    Address = Column("Address")
    Phone = Column("Phone")
    Activity_Subject = Column("ActivitySubject")
    State = Column("State")
    ID = Column("Id")


table_metadata = TableMetadata()


reader = CFIReader(
    url_pattern = "https://cfi.rbcapi.ir/institutes/{id}?offset=0&limit=10&lng=fa",
    table_metadata=table_metadata,
)
