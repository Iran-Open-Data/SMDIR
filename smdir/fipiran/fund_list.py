from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

from ..metadata_reader import Table, Column
from .common import fipiran_directory, FIPReader

# {
#     "status": 200,
#     "message": "",
#     "pageNumber": 1,
#     "pageSize": 437,
#     "totalCount": 437,
#     "items": [
#         {
#             "regNo": "11777",
#             "name": "اختصاصی بازارگردانی آسمان زاگرس",
#             "rankOf12Month": null,
#             "rankOf24Month": null,
#             "rankOf36Month": null,
#             "rankOf48Month": null,
#             "rankOf60Month": null,
#             "rankLastUpdate": "0001-01-01T00:00:00",
#             "fundType": 11,
#             "typeOfInvest": "IssuanceAndCancellation",
#             "fundSize": 65919854335577,
#             "initiationDate": "2021-01-03T00:00:00",
#             "dailyEfficiency": 0,
#             "weeklyEfficiency": 0.949,
#             "monthlyEfficiency": -1.5,
#             "quarterlyEfficiency": -1.756,
#             "sixMonthEfficiency": -20.028,
#             "annualEfficiency": 2736.641,
#             "statisticalNav": 51192770.00,
#             "efficiency": 5019.313,
#             "cancelNav": 51192770.00,
#             "issueNav": 51268698.00,
#             "dividendIntervalPeriod": 0,
#             "guaranteedEarningRate": null,
#             "date": "2024-01-06T00:00:00",
#             "netAsset": 65919854335577,
#             "estimatedEarningRate": null,
#             "investedUnits": 1287679,
#             "articlesOfAssociationLink": null,
#             "prosoectusLink": null,
#             "websiteAddress": [
#                 "azmfund.com"
#             ],
#             "manager": "سبد گردان آسمان",
#             "managerSeoRegisterNo": "10906",
#             "guarantorSeoRegisterNo": null,
#             "auditor": "موسسه حسابرسی هوشیار ممیز",
#             "custodian": "موسسه حسابرسی ارقام نگر آریا",
#             "guarantor": "----",
#             "beta": null,
#             "alpha": null,
#             "isCompleted": true,
#             "fiveBest": 98.870000,
#             "stock": 100.000000,
#             "bond": 0.000000,
#             "other": -0.010000,
#             "cash": 0.000000,
#             "deposit": 0.090000,
#             "fundUnit": null,
#             "commodity": null,
#             "fundPublisher": 1,
#             "smallSymbolName": null,
#             "insCode": null,
#             "fundWatch": null
#         },
#     ]
# }


class _FundIdentity(BaseModel):
    regNo: str
    name: str
    rankOf12Month: Optional[int]
    rankOf24Month: Optional[int]
    rankOf36Month: Optional[int]
    rankOf48Month: Optional[int]
    rankOf60Month: Optional[int]
    rankLastUpdate: Optional[str]
    fundType: Optional[int]
    typeOfInvest: Optional[str]
    fundSize: Optional[int]
    initiationDate: Optional[str]
    dailyEfficiency: Optional[float]
    weeklyEfficiency: Optional[float]
    monthlyEfficiency: Optional[float]
    quarterlyEfficiency: Optional[float]
    sixMonthEfficiency: Optional[float]
    annualEfficiency: Optional[float]
    statisticalNav: Optional[float]
    efficiency: Optional[float]
    cancelNav: Optional[float]
    issueNav: Optional[float]
    dividendIntervalPeriod: Optional[int]
    guaranteedEarningRate: Optional[float]
    date: Optional[str]
    netAsset: Optional[int]
    estimatedEarningRate: Optional[float]
    investedUnits: Optional[int]
    articlesOfAssociationLink: Optional[str]
    prosoectusLink: Optional[str]
    websiteAddress: Optional[list[str]]
    manager: Optional[str]
    managerSeoRegisterNo: Optional[str]
    guarantorSeoRegisterNo: Optional[str]
    auditor: Optional[str]
    custodian: Optional[str]
    guarantor: Optional[str]
    beta: Optional[float]
    alpha: Optional[float]
    isCompleted: Optional[bool]
    fiveBest: Optional[float]
    stock: Optional[float]
    bond: Optional[float]
    other: Optional[float]
    cash: Optional[float]
    deposit: Optional[float]
    fundUnit: Optional[float]
    commodity: Optional[float]
    fundPublisher: Optional[int]
    smallSymbolName: Optional[str]
    insCode: Optional[str]
    fundWatch: None


class Validator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: Literal[200]
    message: str
    pageNumber: Literal[1]
    pageSize: int
    totalCount: int
    items: list[_FundIdentity]


class TableMetadata(Table):
    directory = fipiran_directory
    name = "fund_list"
    records_address = ["items"]
    validator = Validator

    SEO_ID = Column("regNo")
    Name = Column("name")
    RankOf12Month = Column("rankOf12Month")
    RankOf24Month = Column("rankOf24Month")
    RankOf36Month = Column("rankOf36Month")
    RankOf48Month = Column("rankOf48Month")
    RankOf60Month = Column("rankOf60Month")
    RankLastUpdate = Column("rankLastUpdate")
    FundType = Column("fundType")
    TypeOfInvest = Column("typeOfInvest")
    FundSize = Column("fundSize")
    InitiationDate = Column("initiationDate")
    DailyEfficiency = Column("dailyEfficiency")
    WeeklyEfficiency = Column("weeklyEfficiency")
    MonthlyEfficiency = Column("monthlyEfficiency")
    QuarterlyEfficiency = Column("quarterlyEfficiency")
    SixMonthEfficiency = Column("sixMonthEfficiency")
    AnnualEfficiency = Column("annualEfficiency")
    StatisticalNav = Column("statisticalNav")
    Efficiency = Column("efficiency")
    CancelNav = Column("cancelNav")
    IssueNav = Column("issueNav")
    DividendIntervalPeriod = Column("dividendIntervalPeriod")
    GuaranteedEarningRate = Column("guaranteedEarningRate")
    Date = Column("date")
    NetAsset = Column("netAsset")
    EstimatedEarningRate = Column("estimatedEarningRate")
    InvestedUnits = Column("investedUnits")
    ArticlesOfAssociationLink = Column("articlesOfAssociationLink")
    ProsoectusLink = Column("prosoectusLink")
    WebsiteAddress = Column("websiteAddress")
    Manager = Column("manager")
    ManagerSeoRegisterNo = Column("managerSeoRegisterNo")
    GuarantorSeoRegisterNo = Column("guarantorSeoRegisterNo")
    Auditor = Column("auditor")
    Custodian = Column("custodian")
    Guarantor = Column("guarantor")
    Beta = Column("beta")
    Alpha = Column("alpha")
    IsCompleted = Column("isCompleted")
    FiveBest = Column("fiveBest")
    Stock = Column("stock")
    Bond = Column("bond")
    Other = Column("other")
    Cash = Column("cash")
    Deposit = Column("deposit")
    FundUnit = Column("fundUnit")
    Commodity = Column("commodity")
    FundPublisher = Column("fundPublisher")
    SmallSymbolName = Column("smallSymbolName")
    InsCode = Column("insCode")


table_metadata = TableMetadata()

reader = FIPReader(
    url_pattern="https://fund.fipiran.ir/api/v1/fund/fundcompare",
    table_metadata=table_metadata,
)
