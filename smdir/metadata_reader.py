from pathlib import Path
from typing import Callable
import inspect

import pandas as pd
from pydantic import BaseModel
import yaml

package_dir = Path(__file__).parent
root_dir = Path()

default_settings_path = package_dir.joinpath("conf", "default_settings.yaml")
settings_path = package_dir.joinpath("conf", "settings.yaml")
local_setting_path = root_dir.joinpath("smdir_conf.yaml")

settings_dict = {}
with default_settings_path.open(encoding="utf-8") as file:
    settings_dict.update(yaml.safe_load(file))
try:
    with settings_path.open(encoding="utf-8") as file:
        settings_dict.update(yaml.safe_load(file))
except FileNotFoundError:
    pass
try:
    with local_setting_path.open(encoding="utf-8") as file:
        settings_dict.update(yaml.safe_load(file))
except FileNotFoundError:
    pass


def get_metadata(*path_parts: str) -> dict | list:
    parts = ["metadata"] + list(path_parts)
    parts[-1] = parts[-1] + ".yaml"
    caller_path = Path(inspect.stack()[1].filename)
    meta_path = caller_path.parent.joinpath(*parts)
    with meta_path.open(encoding="utf-8") as yaml_file:
        metadata = yaml.safe_load(yaml_file)
    return metadata


def save_metadata(content: dict | list, *path_parts: str) -> None:
    parts = ["metadata"] + list(path_parts)
    parts[-1] = parts[-1] + ".yaml"
    caller_path = Path(inspect.stack()[1].filename)
    meta_path = caller_path.parent.joinpath(*parts)
    with meta_path.open(mode="w", encoding="utf-8") as yaml_file:
        yaml.safe_dump(content, yaml_file, encoding="utf-8", allow_unicode=True)


class Settings(BaseModel):
    data_dir: Path = Path(settings_dict["data_directory"])
    package_name: str = settings_dict["package_name"]
    bucket_address: str = settings_dict["bucket_address"]
    online_dir: str = f"{bucket_address}/{package_name}"


lib_settings = Settings()


class Table:
    directory: Path
    name: str
    api_params: list[str] = []
    records_address: list[str] = []
    partition: list[str] | None = None
    keys: list[str] = []
    validator: Callable | None = None
    keep_history: bool = False
    is_raw_text: bool = False

    def __init__(self) -> None:
        if not self.directory.exists():
            self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory.joinpath(f"{self.name}.parquet")
        self.set_table_in_columns(self)

    def __fspath__(self) -> str:
        return self.path.__fspath__()

    @property
    def raw(self) -> Path:
        return self.path.parent.joinpath(self.path.stem + "_raw" + self.path.suffix)

    @classmethod
    def set_table_in_columns(cls, self) -> None:
        for key, value in cls.__dict__.items():
            if not isinstance(value, Column):
                continue
            setattr(value, "new_name", key)
            setattr(value, "table", self)

    @classmethod
    def get_columns(cls) -> dict:
        return {
            key: value.address
            for key, value in cls.__dict__.items()
            if isinstance(value, Column) and value.address is not None
        }

    def validate_input(self, _input: dict) -> dict:
        if self.validator is None:
            raise ValueError
        # pylint: disable=not-callable
        return self.validator(**_input).model_dump()

    def post_process(self, table: pd.DataFrame) -> pd.DataFrame:
        return table


class Column:
    table: Table
    new_name: str

    def __init__(
        self, address: str | int | list[str | int] | tuple[str | int, ...] | None = None
    ):
        if address is None:
            self.address = address
        elif isinstance(address, str):
            self.address = (address,)
        elif isinstance(address, tuple):
            self.address = address
        elif isinstance(address, list):
            self.address = address
        else:
            raise ValueError
