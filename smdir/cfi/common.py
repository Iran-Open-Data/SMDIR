from ..metadata_reader import lib_settings
from ..datareader import DataReader

cfi_directory = lib_settings.data_dir.joinpath("cfi")

class CFIReader(DataReader):
    headers = {
        "Connection": "keep-alive",
        "Host": "cfi.rbcapi.ir",
        "Origin": "https://cfi.seo.ir",
        "Referer": "https://cfi.seo.ir/",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
    }
