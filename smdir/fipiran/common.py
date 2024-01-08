from ..metadata_reader import lib_settings
from ..datareader import DataReader

fipiran_directory = lib_settings.data_dir.joinpath("fipiran")


class FIPReader(DataReader):
    headers = {
        "Connection": "keep-alive",
        "Host": "fund.fipiran.ir",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
    }
