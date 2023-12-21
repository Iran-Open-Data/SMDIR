from pathlib import Path
import inspect

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
    path_parts = ["metadata"] + list(path_parts)
    path_parts[-1] = path_parts[-1] + ".yaml"
    caller_path = Path(inspect.stack()[1].filename)
    meta_path = caller_path.parent.joinpath(*path_parts)
    with meta_path.open(encoding="utf-8") as yaml_file:
        metadata = yaml.safe_load(yaml_file)
    return metadata


def save_metadata(content: dict | list, *path_parts: str) -> None:
    path_parts = ["metadata"] + list(path_parts)
    path_parts[-1] = path_parts[-1] + ".yaml"
    caller_path = Path(inspect.stack()[1].filename)
    meta_path = caller_path.parent.joinpath(*path_parts)
    with meta_path.open(mode="w", encoding="utf-8") as yaml_file:
        yaml.safe_dump(content, yaml_file, encoding="utf-8", allow_unicode=True)


class Settings(BaseModel):
    data_dir: Path = Path(settings_dict["data_directory"])
    package_name: str = settings_dict["package_name"]
    bucket_address: str = settings_dict["bucket_address"]
    online_dir: str = f"{bucket_address}/{package_name}"

    ifb_dir: Path = data_dir.joinpath("ifb")
    tsetmc_dir: Path = data_dir.joinpath("tsetmc")
    codal_dir: Path = data_dir.joinpath("codal")

    def model_post_init(self, __context=None) -> None:
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self.ifb_dir.mkdir(exist_ok=True)
        self.tsetmc_dir.mkdir(exist_ok=True)
        self.codal_dir.mkdir(exist_ok=True)


lib_settings = Settings()


class IFB(BaseModel):
    folder: Path = lib_settings.ifb_dir
    bond_list: Path = folder.joinpath("bond_list.parquet")
    bond_page: Path = folder.joinpath("bond_page.parquet")
    payment_table: Path = folder.joinpath("payment_table.parquet")
    bond_info: Path = folder.joinpath("bond_info.parquet")


class TSETMC(BaseModel):
    folder: Path = lib_settings.tsetmc_dir
    price: Path = folder.joinpath("price.parquet")
    shareholders: Path = folder.joinpath("shareholders.parquet")


class Tables(BaseModel):
    ifb: IFB = IFB()
    tsetmc: TSETMC = TSETMC()


tables = Tables()
