from datetime import datetime
from pathlib import Path

import requests
import pandas as pd

from .metadata_reader import lib_settings


def add_received_time(table: pd.DataFrame) -> pd.DataFrame:
    table["received_time"] = datetime.now()
    return table


def create_key_form_path(file_path: Path) -> str:
    root_length = len(lib_settings.data_dir.parts)
    name = "/".join(file_path.parts[root_length:])
    url = f"Data/{name}"
    return url


def is_file_up_to_date(file_path: Path) -> bool:
    url = f"{lib_settings.online_dir}/{create_key_form_path(file_path)}"
    response = requests.get(url, timeout=100, stream=True)
    try:
        online_file = int(response.headers["Content-Length"])
    except KeyError:
        online_file = 0

    try:
        local_file = file_path.stat().st_size
    except FileNotFoundError:
        local_file = 0
    return local_file == online_file


def download_file(file_path: Path) -> None:
    url = f"{lib_settings.online_dir}/{create_key_form_path(file_path)}"
    response = requests.get(url, timeout=100)
    with file_path.open(mode="wb") as file:
        file.write(response.content)


class MapTitles:
    def __init__(self, label_map: list[dict[str, str]]) -> None:
        self.label_map = label_map
        self.label_map_copy = self.label_map.copy()

    def map_titles(self, title_list):
        self.label_map_copy = self.label_map.copy()
        label_list = []
        for title in title_list:
            label = self._find_label(title)
            if label is None:
                raise KeyError(f"Title `{title}` not found!")
            label_list.append(label)
        return label_list

    def _find_label(self, title):
        while len(self.label_map_copy) > 0:
            label_dict = self.label_map_copy.pop(0)
            key, value = list(label_dict.items())[0]
            if title == key:
                return value
        return None
