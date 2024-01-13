from dataclasses import dataclass
from typing import Literal

import pandas as pd

from .metadata_reader import Table, Column, get_metadata
from . import utils

from . import tsetmc, ifb


@dataclass
class TSETMC:
    security_identity = tsetmc.security_identity.table_metadata
    daily_closing_price = tsetmc.daily_closing_price.table_metadata
    codal_publisher_info = tsetmc.codal_publisher_info.table_metadata
    shareholders = tsetmc.shareholders.table_metadata


@dataclass
class IFB:
    bond_list = ifb.datareader.bond_list_metadata
    bond_page = ifb.datareader.bond_page_metadata
    bond_info = ifb.datareader.bond_info_metadata
    payment_table = ifb.datareader.payment_table_metadata


@dataclass
class TABLES:
    tsetmc = TSETMC()
    ifb = IFB()


tables = TABLES()


ItamAlias = Literal["Price",]

item_aliases = {
    "Price": tables.tsetmc.daily_closing_price.Closing_Price,
}


def load_table(
    table: Table, columns: list[Column] | None = None, *, update: bool = True
) -> pd.DataFrame:
    if not table.path.exists() or update:
        utils.download_file(table.path)
    if columns is not None:
        column_names = []
        for column in columns:
            assert column.table == table
            column_names.append(column.new_name)
    else:
        column_names = None
    return pd.read_parquet(table, columns=column_names)


def search_security(dataset: pd.DataFrame, security: str) -> pd.DataFrame:
    def match_security(column: pd.Series, string) -> pd.Series:
        return column.str.match(string)

    return dataset.loc[
        dataset.apply(match_security, string=security).any(axis="columns")
    ]


def load_data(
    items: list[Column] | ItamAlias,
    securities: list[str] | str | None = None,
    update: bool = True,
) -> pd.DataFrame:
    if securities is None:
        securitie_list = None
    else:
        securities = [securities] if isinstance(securities, str) else securities
        security_aliases = get_metadata("security_aliases")
        assert isinstance(security_aliases, dict)
        securitie_list = []
        while len(securities) > 0:
            security = securities[0]
            if security in security_aliases:
                assert isinstance(security_aliases[security], list)
                securities.extend(security_aliases[security])
            else:
                securitie_list.append(security)
            securities.pop(0)

    keys = ["INS_Code", "ISIN", "Farsi_Symbol"]
    key_table = load_table(tables.tsetmc.security_identity, update=update)[keys]
    if securitie_list is not None:
        key_table = pd.concat(
            [search_security(key_table, security) for security in securitie_list],
            ignore_index=True,
        )
    key_table = key_table.set_index(keys)

    columns_to_get = []
    for item in items:
        if item in item_aliases:
            columns_to_get.append(item_aliases[item])
        elif isinstance(item, Column):
            columns_to_get.append(item)
        else:
            raise ValueError
    tables_to_get: dict[Table, list[Column]] = {}
    for column in columns_to_get:
        if column.table not in tables_to_get:
            tables_to_get[column.table] = []
            for key in column.table.keys:
                tables_to_get[column.table].append(getattr(column.table, key))
        if column in tables_to_get[column.table]:
            continue
        tables_to_get[column.table].append(column)
    table_list = [
        load_table(table, columns, update=update).set_index(table.keys)
        for table, columns in tables_to_get.items()
    ]
    for table in table_list:
        key_table = key_table.join(table)
    return key_table
