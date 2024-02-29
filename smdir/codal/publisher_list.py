"""
Codal firm list scraper
"""

import time
import urllib.parse

from bs4 import BeautifulSoup
import requests
import pandas as pd

from ..metadata_reader import Table, Column
from .common import codal_directory, CodalReader


class Scraper:
    """Codal firm list scraper"""

    url = "https://www.codal.ir/CompanyList.aspx"

    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8,fa;q=0.7",
        "Connection": "keep-alive",
        "Origin": "https://www.codal.ir",
        "Referer": "https://www.codal.ir/CompanyList.aspx",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        ),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    data = {
        "ctl00$ScriptManager1": (
            "ctl00$ContentPlaceHolder1$UpdatePanel1|"
            "ctl00$ContentPlaceHolder1$ucPager1$btnNext"
        ),
        "__ASYNCPOST": "true",
        "ctl00$ContentPlaceHolder1$ucPager1$btnNext": "",
    }

    def __init__(self) -> None:
        self.response = requests.get(url=self.url, headers=self.headers, timeout=10)
        self.cookies = self.extract_cookies()
        self.soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        self.data.update(self.extract_hidden_inputs())
        self.last_page = int(
            self.soup.find(
                "span", {"id": "ctl00_ContentPlaceHolder1_ucPager1_lblTotalPages"}
            ).text  # type: ignore
        )

    def update_cookies(self):
        """Update Cookes"""
        if "Set-Cookie" in self.response.headers:
            self.cookies = self.extract_cookies()

    def extract_cookies(self):
        """Extract Cookes"""
        cookie_parts = self.response.headers["Set-Cookie"].split(" ")
        cookie_parts = [
            cookie_part.strip(";")
            for cookie_part in cookie_parts
            if all(
                [
                    cookie_part.find(";") >= 0,
                    cookie_part.find("=") >= 0,
                    cookie_part.find("ath=/") < 0,
                ]
            )
        ]
        cookies = {"Culture": "CultureName=fa-IR"}
        cookies.update(dict(cookie_part.split("=") for cookie_part in cookie_parts))
        return cookies

    def extract_hidden_inputs(self, update=False):
        """Extract Hidden Input from Html Script"""
        hidden_inputs = self.soup.find_all("input", {"type": "hidden"})
        hidden_inputs = {
            hidden_input["name"]: hidden_input["value"]
            if "value" in hidden_input.attrs
            else ""
            for hidden_input in hidden_inputs
        }
        if update:
            hidden_inputs.update(self.update_hidden_input_variables())
        return hidden_inputs

    def update_hidden_input_variables(self):
        """Update Hidden Input Variables"""
        variable_change_list = (
            str(self.response.content)
            .rsplit("\\n", maxsplit=1)[1]
            .strip()
            .split(",")[0]
            .split("|")
        )
        hidden_inputs = {}
        for variable in [
            "__EVENTTARGET",
            "__EVENTARGUMENT",
            "__VIEWSTATE",
            "__VIEWSTATEGENERATOR",
            "__VIEWSTATEENCRYPTED",
            "__EVENTVALIDATION",
        ]:
            variable_index = variable_change_list.index(variable)
            hidden_inputs[variable_change_list[variable_index]] = variable_change_list[
                variable_index + 1
            ]
        return hidden_inputs

    @property
    def current_page(self):
        """Return Current Page"""
        page = int(self.soup.find("input", {"class": "selected"})["value"])  # type: ignore
        return page

    def _go_to_next_page(self):
        old_page = self.current_page
        while True:
            time.sleep(0.1)
            try:
                self.response = requests.post(
                    url=self.url,
                    cookies=self.cookies,
                    headers=self.headers,
                    data=self.data,
                    timeout=10,
                )
                break
            except requests.ConnectionError:
                pass
        self.update_cookies()
        self.soup = BeautifulSoup(self.response.content.decode(), "html.parser")
        self.data.update(self.extract_hidden_inputs(update=True))
        return old_page + 1 == self.current_page

    def _extract_table(self):
        def clean_text(text):
            for char in ("\n", "\t"):
                text = text.replace(char, "")
            text = text.strip()
            return text

        html_rows = self.soup.find_all("tr")[1:]

        table = []
        for inp_row in html_rows:
            cells = inp_row.find_all("td")
            try:
                reports = (
                    "https://codal.ir/" + cells[3].contents[1].contents[3].a["href"]
                )
            except TypeError:
                reports = None
            try:
                website = cells[3].contents[1].contents[1].a["href"]
            except TypeError:
                website = None
            outp_row = [
                clean_text(cells[0].text),
                clean_text(cells[1].text),
                cells[2].text,
                "https://codal.ir/" + cells[0].a["href"],
                reports,
                website,
            ]
            table.append(outp_row)
        table = pd.DataFrame(table)
        table.columns = ["Symbol", "Name", "ISIC", "Page_URL", "Reports_URL", "Website"]
        return table

    def extract(self):
        tables = [self._extract_table()]
        while self.current_page < self.last_page:
            result = self._go_to_next_page()
            if not result:
                raise ValueError
            tables.append(self._extract_table())
        publishers_list = pd.concat(tables, ignore_index=True)
        publishers_list["ISIC"] = (
            publishers_list["ISIC"].replace("\xa0", None).astype("string")
        )
        return publishers_list

    def get_dict(self) -> dict:
        table = self.extract()
        output = {"records": table.to_dict("records")}
        return output


def add_symbol_id_column(table: pd.DataFrame) -> pd.DataFrame:
    return table.assign(
        Page_Symbol_ID=(
            table["Page_URL"]
            .str.split("Symbol=", expand=True)[1]
            .apply(urllib.parse.unquote)
        ),
        Search_Symbol_ID=(
            table["Reports_URL"]
            .str.split("Symbol=", expand=True)[1]
            .apply(urllib.parse.unquote)
        ),
    )


class TableMetadata(Table):
    directory = codal_directory
    name = "publisher_list"
    records_address = ["records"]
    keep_history = False

    Symbol = Column("Symbol")
    Name = Column("Name")
    ISIC = Column("ISIC")
    Page_URL = Column("Page_URL")
    Reports_URL = Column("Reports_URL")
    Website = Column("Website")

    def post_process(self, table: pd.DataFrame) -> pd.DataFrame:
        return add_symbol_id_column(table)


table_metadata = TableMetadata()


class CodalPublisherListReader(CodalReader):
    def get(self, **kwargs):
        return Scraper().get_dict()


reader = CodalPublisherListReader(
    url_pattern="",
    table_metadata=table_metadata,
)
