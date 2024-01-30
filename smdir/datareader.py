from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
import random
import json
import itertools

import requests

# import requests.exceptions
from requests.models import Response
import pandas as pd

from . import utils
from .metadata_reader import Table


class DataReader:
    headers: dict

    def __init__(self, url_pattern: str, table_metadata: Table) -> None:
        self.table_metadata = table_metadata
        for key in self.table_metadata.api_params:
            assert f"{{{key}}}" in url_pattern
        self.url_pattern = url_pattern
        self.raw_path = self.table_metadata.raw

    def get(self, retry: int = 0, **kwargs) -> dict:
        for key in self.table_metadata.api_params:
            assert key in kwargs
        url = self.url_pattern.format(**kwargs)
        try:
            response = requests.get(url=url, headers=self.headers, timeout=100)
        except requests.exceptions.RequestException:
            retry += 1
            print(f"Getting data failed for {kwargs}. Retrying ... ({retry})")
            if retry == 0:
                time.sleep(20 + random.random() * 80)
            else:
                time.sleep(1)
            if retry < 5:
                return self.get(retry=retry, **kwargs)
            return {}
        if self.table_metadata.is_raw_text:
            return {"text": response.text}
        try:
            result = self.parse(response)
        except (json.JSONDecodeError, requests.exceptions.RequestException):
            retry += 1
            print(f"Parsing data failed for {kwargs}. Retrying ... ({retry})")
            print(response.content)
            if retry == 0:
                time.sleep(20 + random.random() * 80)
            else:
                time.sleep(1)
            if retry < 5:
                return self.get(retry=retry, **kwargs)
            return {}
        if self.table_metadata.validator is not None:
            result = self.table_metadata.validate_input(result)
        assert isinstance(result, dict)
        return result

    @staticmethod
    def parse(response: Response) -> dict:
        result = response.json()
        assert isinstance(result, dict)
        return result

    def create_raw_row(self, row: pd.Series = pd.Series()) -> pd.Series:
        keys = row[self.table_metadata.api_params].to_dict()
        keys.update(
            {
                "JSON": json.dumps(self.get(**keys), ensure_ascii=False),
                "recived_time": datetime.now(),
            }
        )
        return pd.Series(keys)

    def create_raw_table(
        self, key_frame: pd.DataFrame = pd.DataFrame()
    ) -> pd.DataFrame:
        if key_frame.empty:
            return self.create_raw_row().to_frame().transpose()
        key_frame = key_frame.copy()
        key_frame.columns = key_frame.columns.str.lower()
        for key in self.table_metadata.api_params:
            assert key in key_frame.columns
        number = len(key_frame) // 20 + 1
        with ThreadPoolExecutor(max_workers=8) as executor:
            raw_table = pd.concat(
                executor.map(
                    lambda df: df.apply(self.create_raw_row, axis=1),
                    utils.split_dataframe(key_frame, n=number),
                ),
                ignore_index=True,
            )
        return raw_table

    def update_raw_table(
        self, key_frame: pd.DataFrame = pd.DataFrame(), *, ignore_existing=True
    ) -> None:
        if key_frame.empty:
            self._update_raw_table_part(key_frame)
            return

        params_list = self.table_metadata.api_params
        key_frame = key_frame.copy()
        key_frame.columns = key_frame.columns.str.lower()
        key_frame = key_frame[params_list].drop_duplicates()
        if ignore_existing and self.raw_path.exists():
            key_frame["ToGet"] = 1
            existing_keys = pd.read_parquet(self.raw_path, columns=params_list)
            key_frame = (
                pd.concat([key_frame, existing_keys])
                .drop_duplicates(params_list, keep=False)
                .loc[lambda df: df["ToGet"] == 1]
                .drop(columns=["ToGet"])
            )
            if len(key_frame.index) == 0:
                return
        print(f"{len(key_frame)} records to get")
        number = (len(key_frame) - 1) // 5000 + 1
        key_frame_parts = utils.split_dataframe(key_frame, number)
        for part in key_frame_parts:
            self._update_raw_table_part(part)

    def _update_raw_table_part(self, key_frame: pd.DataFrame) -> None:
        try:
            old_table = pd.read_parquet(self.raw_path)
        except FileNotFoundError:
            old_table = pd.DataFrame()
        new_table = self.create_raw_table(key_frame)
        columns = new_table.columns.to_list()
        columns.remove("recived_time")
        table = (
            pd.concat([old_table, new_table], ignore_index=True)
            .sort_values("recived_time", ascending=False)
            .drop_duplicates(columns, keep="last")
            .reset_index(drop=True)
        )
        table.to_parquet(
            self.raw_path, partition_cols=self.table_metadata.partition, index=False
        )

    def create_table(self) -> pd.DataFrame:
        records = pd.read_parquet(self.raw_path).sort_values(
            "recived_time", ascending=False
        )
        if len(self.table_metadata.api_params) > 0:
            records = records.drop_duplicates(self.table_metadata.api_params)
        else:
            records = records.iloc[:1, :]
        records = records.apply(self.create_records, axis=1)  # type: ignore
        records = itertools.chain.from_iterable(records)
        table = pd.DataFrame.from_records(records)
        table = self.table_metadata.post_process(table)
        return table

    def create_records(self, row: pd.Series) -> list[dict]:
        data = json.loads(row["JSON"])
        if data == {}:
            return []
        api_params = row[self.table_metadata.api_params].to_dict()
        for address_part in self.table_metadata.records_address:
            data = data[address_part]
        if isinstance(data, dict):
            data = [data]
        records = []
        for raw_record in data:
            record = api_params.copy()
            record.update(self._create_record(raw_record))
            records.append(record)
        return records

    def _create_record(self, raw_record: dict) -> dict:
        record = {}
        for name, original_name in self.table_metadata.get_columns().items():
            value = raw_record
            for key in original_name:
                try:
                    value = value[key]
                except IndexError:
                    value = None
                    break
            record[name] = value
        return record

    def update_table(self) -> None:
        table = self.create_table()
        table.to_parquet(self.table_metadata.path, index=False)

    def open_table(self) -> pd.DataFrame:
        return pd.read_parquet(self.table_metadata.path)
