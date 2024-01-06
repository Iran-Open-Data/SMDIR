from ..metadata_reader import lib_settings
from ..datareader import DataReader

tsetmc_directory = lib_settings.data_dir.joinpath("tsetmc")


class TSETMCReader(DataReader):
    headers = {
        "Connection": "keep-alive",
        "Host": "cdn.tsetmc.com",
        "Origin": "http://www.tsetmc.com",
        "Referer": "http://www.tsetmc.com/",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
    }
