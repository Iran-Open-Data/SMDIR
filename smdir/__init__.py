from pathlib import Path

import pandas as pd

from .metadata_reader import tables
from . import utils


def load_table(table: Path, update: bool = False) -> pd.DataFrame:
    if not table.exists() or update:
        utils.download_file(table)
    return pd.read_parquet(table)
