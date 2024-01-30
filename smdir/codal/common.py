from ..metadata_reader import lib_settings
from ..datareader import DataReader

codal_directory = lib_settings.data_dir.joinpath("codal")


class CodalReader(DataReader):
    headers = {
        "Connection": "keep-alive",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
    }
