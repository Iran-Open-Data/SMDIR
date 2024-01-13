from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict

from ..metadata_reader import Table, Column
from .common import fipiran_directory, FIPReader

# {
#     "status": 200,
#     "message": "",
#     "item": {
#         "regNo": "11513",
#         "name": "در اوراق بهادار با درآمد ثابت کمند",
#         "initiationDate": "2017-08-21T00:00:00",
#         "fundSize": 86952874149765,
#         "fundType": 4,
#         "executiveManager": "",
#         "articlesOfAssociationLink": null,
#         "prosoectusLink": null,
#         "lastModificationTime": "2024-01-07T09:23:08.9025596",
#         "date": "2024-01-06T00:00:00",
#         "dailyEfficiency": 0.07,
#         "weeklyEfficiency": 0.59,
#         "monthlyEfficiency": 2.11,
#         "quarterlyEfficiency": 6.15,
#         "sixMonthEfficiency": 12.14,
#         "annualEfficiency": 24.2,
#         "dividendIntervalPeriod": 1,
#         "estimatedEarningRate": null,
#         "guaranteedEarningRate": null,
#         "insInvNo": 3,
#         "insInvPercent": 100.00,
#         "legalPercent": 100.00,
#         "marketMaker": "صندوق بازارگردانی اکسیر سودا",
#         "naturalPercent": 0.00,
#         "netAsset": 86952874149765,
#         "retInvNo": 0,
#         "retInvPercent": 0.00,
#         "investedUnits": 8688400000,
#         "unitsRedDAY": 0,
#         "unitsRedFromFirst": 89126600000,
#         "unitsSubDAY": 0,
#         "unitsSubFromFirst": 106732069182,
#         "efficiency": 132.7,
#         "cancelNav": 10007.00,
#         "issueNav": 10021.00,
#         "statisticalNav": 10344.00,
#         "fiveBest": 3.520000,
#         "stock": 7.950000,
#         "bond": 41.950000,
#         "other": 0.640000,
#         "cash": 0.010000,
#         "deposit": 38.090000,
#         "fundUnit": 11.220000,
#         "commodity": 0.130000,
#         "typeOfInvest": "Negotiable",
#         "rankOf12Month": null,
#         "rankOf24Month": null,
#         "rankOf36Month": null,
#         "rankOf48Month": null,
#         "rankOf60Month": null,
#         "rankLastUpdate": "0001-01-01T00:00:00",
#         "manager": "سبد گردان کاریزما",
#         "managerSeoRegisterNo": "10856",
#         "guarantorSeoRegisterNo": null,
#         "auditor": "موسسه حسابرسی و خدمات مدیریت ارقام نگر آریا",
#         "websiteAddress": [
#             "kamandfixedincome.com"
#         ],
#         "custodian": "موسسه حسابرسی رازدار",
#         "guarantor": "----",
#         "investmentManager": "میثم زارعی، شیرین معطر تهرانی، محمدرضا خانی معصوم آباد علیا",
#         "beta": null,
#         "alpha": null,
#         "fundWatch": null,
#         "seoRegisterDate": "2017-06-25T00:00:00",
#         "registrationNumber": "41928",
#         "registerDate": "2017-06-19T00:00:00",
#         "nationalId": "14006847020",
#         "isCompleted": true,
#         "insCode": "34718633636164421",
#         "fundPublisher": 2,
#         "mutualFundLicenses": [
#             {
#                 "id": 249986,
#                 "regNo": "11513",
#                 "isExpired": false,
#                 "startDate": "2017-08-21T00:00:00",
#                 "expireDate": null,
#                 "licenseNo": "41928",
#                 "licenseStatusId": 1,
#                 "licenseStatusDescription": null,
#                 "licenseTypeId": 23,
#                 "newLicenseTypeId": null,
#                 "mutualFund": null
#             }
#         ]
#     }
# }


class _License(BaseModel):
    id: int
    regNo: str
    isExpired: Optional[bool]
    startDate: Optional[str]
    expireDate: Optional[str]
    licenseNo: Optional[str]
    licenseStatusId: Optional[int]
    licenseStatusDescription: Optional[str]
    licenseTypeId: Optional[int]
    newLicenseTypeId: Optional[int]
    mutualFund: None


class _FundIdentity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    regNo: str
    name: str
    initiationDate: Optional[str]
    fundSize: Optional[int]
    fundType: Optional[int]
    executiveManager: Optional[str]
    articlesOfAssociationLink: Optional[str]
    prosoectusLink: Optional[str]
    lastModificationTime: Optional[str]
    date: Optional[str]
    dailyEfficiency: Optional[float]
    weeklyEfficiency: Optional[float]
    monthlyEfficiency: Optional[float]
    quarterlyEfficiency: Optional[float]
    sixMonthEfficiency: Optional[float]
    annualEfficiency: Optional[float]
    dividendIntervalPeriod: Optional[int]
    estimatedEarningRate: Optional[float]
    guaranteedEarningRate: Optional[float]
    insInvNo: Optional[int]
    insInvPercent: Optional[float]
    legalPercent: Optional[float]
    marketMaker: Optional[str]
    naturalPercent: Optional[float]
    netAsset: Optional[int]
    retInvNo: Optional[int]
    retInvPercent: Optional[float]
    investedUnits: Optional[int]
    unitsRedDAY: Optional[int]
    unitsRedFromFirst: Optional[int]
    unitsSubDAY: Optional[int]
    unitsSubFromFirst: Optional[int]
    efficiency: Optional[float]
    cancelNav: Optional[float]
    issueNav: Optional[float]
    statisticalNav: Optional[float]
    fiveBest: Optional[float]
    stock: Optional[float]
    bond: Optional[float]
    other: Optional[float]
    cash: Optional[float]
    deposit: Optional[float]
    fundUnit: Optional[float]
    commodity: Optional[float]
    typeOfInvest: Optional[str]
    rankOf12Month: Optional[int]
    rankOf24Month: Optional[int]
    rankOf36Month: Optional[int]
    rankOf48Month: Optional[int]
    rankOf60Month: Optional[int]
    rankLastUpdate: Optional[str]
    manager: Optional[str]
    managerSeoRegisterNo: Optional[str]
    guarantorSeoRegisterNo: Optional[str]
    auditor: Optional[str]
    websiteAddress: Optional[list[str]]
    custodian: Optional[str]
    guarantor: Optional[str]
    investmentManager: Optional[str]
    beta: Optional[float]
    alpha: Optional[float]
    fundWatch: None
    seoRegisterDate: Optional[str]
    registrationNumber: Optional[str]
    registerDate: Optional[str]
    nationalId: Optional[str]
    isCompleted: Optional[bool]
    insCode: Optional[str]
    fundPublisher: Optional[int]
    mutualFundLicenses: list[_License]


class Validator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    status: Literal[200]
    message: str
    item: _FundIdentity


class TableMetadata(Table):
    directory = fipiran_directory
    name = "fund"
    records_address = ["item"]
    api_params = ["seo_id"]
    validator = Validator

    SEO_ID = Column("regNo")
    Name = Column("name")
    InitiationDate = Column("initiationDate")
    FundSize = Column("fundSize")
    FundType = Column("fundType")
    ExecutiveManager = Column("executiveManager")
    ArticlesOfAssociationLink = Column("articlesOfAssociationLink")
    ProsoectusLink = Column("prosoectusLink")
    LastModificationTime = Column("lastModificationTime")
    Date = Column("date")
    DailyEfficiency = Column("dailyEfficiency")
    WeeklyEfficiency = Column("weeklyEfficiency")
    MonthlyEfficiency = Column("monthlyEfficiency")
    QuarterlyEfficiency = Column("quarterlyEfficiency")
    SixMonthEfficiency = Column("sixMonthEfficiency")
    AnnualEfficiency = Column("annualEfficiency")
    DividendIntervalPeriod = Column("dividendIntervalPeriod")
    EstimatedEarningRate = Column("estimatedEarningRate")
    GuaranteedEarningRate = Column("guaranteedEarningRate")
    InsInvNo = Column("insInvNo")
    InsInvPercent = Column("insInvPercent")
    LegalPercent = Column("legalPercent")
    MarketMaker = Column("marketMaker")
    NaturalPercent = Column("naturalPercent")
    NetAsset = Column("netAsset")
    RetInvNo = Column("retInvNo")
    RetInvPercent = Column("retInvPercent")
    InvestedUnits = Column("investedUnits")
    UnitsRedDAY = Column("unitsRedDAY")
    UnitsRedFromFirst = Column("unitsRedFromFirst")
    UnitsSubDAY = Column("unitsSubDAY")
    UnitsSubFromFirst = Column("unitsSubFromFirst")
    Efficiency = Column("efficiency")
    CancelNav = Column("cancelNav")
    IssueNav = Column("issueNav")
    StatisticalNav = Column("statisticalNav")
    FiveBest = Column("fiveBest")
    Stock = Column("stock")
    Bond = Column("bond")
    Other = Column("other")
    Cash = Column("cash")
    Deposit = Column("deposit")
    FundUnit = Column("fundUnit")
    Commodity = Column("commodity")
    TypeOfInvest = Column("typeOfInvest")
    RankOf12Month = Column("rankOf12Month")
    RankOf24Month = Column("rankOf24Month")
    RankOf36Month = Column("rankOf36Month")
    RankOf48Month = Column("rankOf48Month")
    RankOf60Month = Column("rankOf60Month")
    RankLastUpdate = Column("rankLastUpdate")
    Manager = Column("manager")
    ManagerSeoRegisterNo = Column("managerSeoRegisterNo")
    GuarantorSeoRegisterNo = Column("guarantorSeoRegisterNo")
    Auditor = Column("auditor")
    WebsiteAddress = Column(("websiteAddress", 0))
    Custodian = Column("custodian")
    Guarantor = Column("guarantor")
    InvestmentManager = Column("investmentManager")
    Beta = Column("beta")
    Alpha = Column("alpha")
    FundWatch = Column("fundWatch")
    SeoRegisterDate = Column("seoRegisterDate")
    RegistrationNumber = Column("registrationNumber")
    RegisterDate = Column("registerDate")
    NationalId = Column("nationalId")
    IsCompleted = Column("isCompleted")
    InsCode = Column("insCode")
    FundPublisher = Column("fundPublisher")


table_metadata = TableMetadata()

reader = FIPReader(
    url_pattern="https://fund.fipiran.ir/api/v1/fund/getfund?regno={seo_id}",
    table_metadata=table_metadata,
)
