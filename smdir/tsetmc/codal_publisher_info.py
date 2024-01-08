from typing import Optional
from pydantic import BaseModel, ConfigDict

from .common import TSETMCReader, tsetmc_directory
from ..metadata_reader import Table, Column


# {
#     "codalPublisher": {
#         "id": 6638,
#         "symbol": "فجر",
#         "displaySymbol": "فجر",
#         "name": "فولاد امیر کبیر کاشان",
#         "isic": "271021",
#         "reportingType": "1000000",
#         "executiveManager": "شهرام عالي وند",
#         "address": "کاشان کیلومتر 14 جاده اردستان ",
#         "telNo": "031-55503841-7",
#         "faxNo": "031-55503848",
#         "activitySubject": "\r\n\r\nطراحی، ساخت، راه‌اندازی و بهره‌برداری از
#             کارخانجات تولید ورق نورد گرم وسرد ورقهای فولادی ، ورق رنگی ،
#             ورق اسیدشویی ، قلع اندود، ورقهای گالوانیزه و تولید انواع شمش و
#             تولید انواع محصولات فولادی و شکل دهی انواع ورقهای فولادی.تهیه
#             وتولید انواع فرآورده های شیمیایی ، معدنی وآلی مورد نیاز
#             کارخانجات مذکور در بند موضوعات اصلی.\r\n",
#         "officeAddress": "تهران خیابان ولیعصر مقابل پارک ملت خیابان سایه
#             خیابان مهرشاد ساختمان صداقت طبقه 3",
#         "shareOfficeAddress": "کاشان -کارخانه  صندوق پستی 1534
#             تلفن7 - 55503841 - 031   و  نمابر  55503848 - 031",
#         "website": "www.amirkabirsteelco.ir",
#         "email": "info@amirkabirsteelco.ir",
#         "state": "0",
#         "companyType": "0",
#         "stateName": null,
#         "inspector": "کاربرد تحقيق",
#         "auditorName": "موسسه حسابرسی رازدار",
#         "inspListedCapitalector": null,
#         "listedCapital": "8458000",
#         "financialYear": "12/30",
#         "companyId": null,
#         "financialManager": "محمد نیکساز",
#         "enActivitySubject": null,
#         "enAddress": null,
#         "enDisplayedSymbol": null,
#         "enExecutiveManager": null,
#         "enFinancialManager": null,
#         "enInspector": null,
#         "enName": null,
#         "enOfficeAddress": null,
#         "enShareOfficeAddress": null,
#         "managementGroup": null,
#         "enManagementGroup": null,
#         "nationalCode": "10260206130",
#         "companyType1": null
#     }
# }


class _CodalPublisher(BaseModel):
    symbol: str
    displaySymbol: Optional[str]
    name: Optional[str]
    isic: Optional[str]
    reportingType: Optional[str]
    executiveManager: Optional[str]
    address: Optional[str]
    telNo: Optional[str]
    faxNo: Optional[str]
    activitySubject: Optional[str]
    officeAddress: Optional[str]
    shareOfficeAddress: Optional[str]
    website: Optional[str]
    email: Optional[str]
    state: Optional[str]
    companyType: Optional[str]
    stateName: Optional[str]
    inspector: Optional[str]
    auditorName: Optional[str]
    inspListedCapitalector: Optional[str]
    listedCapital: Optional[str]
    financialYear: Optional[str]
    companyId: Optional[str]
    financialManager: Optional[str]
    enActivitySubject: Optional[str]
    enAddress: Optional[str]
    enDisplayedSymbol: Optional[str]
    enExecutiveManager: Optional[str]
    enFinancialManager: Optional[str]
    enInspector: Optional[str]
    enName: Optional[str]
    enOfficeAddress: Optional[str]
    enShareOfficeAddress: Optional[str]
    managementGroup: Optional[str]
    enManagementGroup: Optional[str]
    nationalCode: Optional[str]
    companyType1: Optional[str]


class Validator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    codalPublisher: _CodalPublisher


class TableMetadata(Table):
    directory = tsetmc_directory
    name = "codal_publisher_info"
    api_params = ["farsi_symbol"]
    records_address = ["codalPublisher"]
    validator = Validator

    Symbol = Column("symbol")
    displaySymbol = Column("displaySymbol")
    Name = Column("name")
    ISIC = Column("isic")
    reportingType = Column("reportingType")
    executiveManager = Column("executiveManager")
    Address = Column("address")
    telNo = Column("telNo")
    faxNo = Column("faxNo")
    activitySubject = Column("activitySubject")
    officeAddress = Column("officeAddress")
    shareOfficeAddress = Column("shareOfficeAddress")
    Website = Column("website")
    Email = Column("email")
    state = Column("state")
    companyType = Column("companyType")
    stateName = Column("stateName")
    inspector = Column("inspector")
    auditorName = Column("auditorName")
    inspListedCapitalector = Column("inspListedCapitalector")
    listedCapital = Column("listedCapital")
    financialYear = Column("financialYear")
    companyId = Column("companyId")
    financialManager = Column("financialManager")
    enActivitySubject = Column("enActivitySubject")
    enAddress = Column("enAddress")
    enDisplayedSymbol = Column("enDisplayedSymbol")
    enExecutiveManager = Column("enExecutiveManager")
    enFinancialManager = Column("enFinancialManager")
    enInspector = Column("enInspector")
    enName = Column("enName")
    enOfficeAddress = Column("enOfficeAddress")
    enShareOfficeAddress = Column("enShareOfficeAddress")
    managementGroup = Column("managementGroup")
    enManagementGroup = Column("enManagementGroup")
    nationalCode = Column("nationalCode")
    companyType1 = Column("companyType1")


table_metadata = TableMetadata()


reader = TSETMCReader(
    url_pattern="https://cdn.tsetmc.com/api/Codal/GetCodalPublisherBySymbol/{farsi_symbol}",
    table_metadata=table_metadata,
)
