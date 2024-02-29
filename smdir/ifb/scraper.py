from bs4 import BeautifulSoup
import requests
import pandas as pd

from ..metadata_reader import get_metadata
from ..utils import MapTitles


def clean_cell_text(cell_text: str):
    for character in ["\r", "\n", "\xa0"]:
        cell_text = cell_text.replace(character, "")
    cell_text = cell_text.strip()
    try:
        cell_text = str(int(cell_text.replace(",", "")))  # type: ignore
    except ValueError:
        pass
    return cell_text


class _IFBBaseScraper:
    PAGINATION_ID = None
    CHANGE_PAGE_EVENT_TARGET = None

    column_rename: str = ""

    def __init__(self, url: str) -> None:
        self.url = url
        self.response = None
        self.soup: BeautifulSoup
        if self.column_rename != "":
            column_rename = get_metadata(self.column_rename)
            assert isinstance(column_rename, dict)
            self.columns_translation: dict = column_rename

        self._get_page()

    def _get_page(self) -> None:
        self.response = requests.get(self.url, allow_redirects=False, timeout=1000)
        if self.response.status_code != 200:
            raise ValueError
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def read_page_status(self) -> tuple[int, int | None]:
        """Function docstring"""
        page_list = (
            self.soup.find("tr", {"class": "pgr"})
            .find("td")  # type: ignore
            .find("tr")  # type: ignore
            .find_all("td")  # type: ignore
        )
        current_page = [
            int(page.find("span").text)
            for page in page_list
            if page.find("span") is not None
        ][0]
        if page_list[-1].text == "...":
            total_pages = None
        else:
            total_pages = int(page_list[-1].text)
        return current_page, total_pages

    def read_selected_pagination(self):
        """Function docstring"""

        def is_selected(element):
            try:
                if element["selected"] == "selected":
                    return True
            except KeyError:
                pass
            return False

        options = self.soup.find("div", {"class": "sizeselector"})
        options = options.find_all("option")  # type: ignore
        selected_option = None
        for option in options:
            if is_selected(option):
                selected_option = int(option["value"])
                break
        if selected_option is None:
            raise ValueError
        return selected_option

    def change_pagination(self, records_per_page: int = 50):
        """function docstring"""
        params = self._prepare_change_pagination_params(records_per_page)
        self.response = requests.post(self.url, data=params, timeout=10)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        return records_per_page == self.read_selected_pagination()

    def _prepare_change_pagination_params(self, records_per_page: int):
        record_number_param = self._extract_record_number_param()
        params = {
            "__EVENTTARGET": record_number_param,
            record_number_param: records_per_page,
        }
        params.update(self._extract_view_states())
        return params

    def change_page(self, page_number: int) -> None:
        """function docstring"""
        params = self._prepare_change_page_params(page_number)
        self.response = requests.post(self.url, data=params, timeout=10)
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def _prepare_change_page_params(self, page_number: int):
        params = {
            "__EVENTTARGET": self.CHANGE_PAGE_EVENT_TARGET,
            "__EVENTARGUMENT": f"Page${page_number}",
        }
        params.update(self._extract_view_states())
        return params

    def _extract_view_states(self):
        hidden_inputs = self.soup.find_all("input", {"type": "hidden"})
        view_states = {}
        for hidden_input in hidden_inputs:
            try:
                view_states[hidden_input["name"]] = hidden_input["value"]
            except KeyError:
                pass
        return view_states

    def _extract_record_number_param(self):
        self.soup.find_all("select")
        select_elements = self.soup.find_all("select")
        parameter_name = None
        for element in select_elements:
            try:
                name = element["name"]
                if name.find(self.PAGINATION_ID) >= 0:
                    parameter_name = name
            except KeyError:
                pass
        if parameter_name is None:
            raise ValueError("Pagination Element not found!")
        return parameter_name

    def extract_page_table(self) -> pd.DataFrame:
        return pd.DataFrame()

    def extract_table(self) -> pd.DataFrame:
        current_page, total_pages = self.read_page_status()
        if current_page != total_pages:
            self.change_pagination()
        table_pages = []
        while True:
            page_table = self.extract_page_table()
            if page_table.empty:
                return page_table
            current_page, total_pages = self.read_page_status()
            table_pages.append(page_table)
            if (total_pages is None) or (current_page < total_pages):
                self.change_page(current_page + 1)
            else:
                break
        table = pd.concat(table_pages, ignore_index=True)
        return table


class ListScraper(_IFBBaseScraper):
    """
    class docstring
    """

    PAGINATION_ID = "ctl00$ContentPlaceHolder1$grdFinancialData$"
    CHANGE_PAGE_EVENT_TARGET = "ctl00$ContentPlaceHolder1$grdFinancialData"

    column_rename = "list_columns"

    def extract_page_table(self) -> pd.DataFrame:
        """docs"""
        table = self.soup.find("table", {"class": "mGrid"}).find_all("tr")  # type: ignore
        columns = table[0].find_all("th")
        columns = [self.columns_translation[column.text] for column in columns]  # type: ignore
        rows = table[1:-2]

        record_ids = [row.find_all("td")[1].find("a")["href"] for row in rows]
        record_ids = [int(row.split("id=")[-1]) for row in record_ids]

        document_id = [int(row.find("i")["onclick"].split("'")[1]) for row in rows]

        cells = [
            [clean_cell_text(cell.text) for cell in row.find_all("td")] for row in rows
        ]

        table = pd.concat(
            [
                pd.DataFrame(record_ids, columns=["IFB_ID"]),
                pd.DataFrame(document_id, columns=["Document_ID"]),
                pd.DataFrame(cells, columns=columns),
            ],
            axis="columns",
        )
        table = table.replace("", None)
        return table


class PageScraper(_IFBBaseScraper):
    PAGINATION_ID = "ctl00$ContentPlaceHolder1$grdPBs"
    CHANGE_PAGE_EVENT_TARGET = "ctl00$ContentPlaceHolder1$grdPBs"
    TABLE_ID = "ContentPlaceHolder1_grdPBs"

    def __init__(self, record_id: int):
        self.record_id = record_id

        url = f"https://ifb.ir/InstrumentsMFI.aspx?id={record_id}"
        super().__init__(url)

    def create_record(self) -> tuple[int, str, dict[str, list]]:
        self._get_page()
        page_str = str(self.soup)
        payment_table = self.extract_table().to_dict("list")
        return (self.record_id, page_str, payment_table)  # type: ignore

    def extract_page_table(self) -> pd.DataFrame:
        """docs"""
        table_rows = self.soup.find("table", {"id": self.TABLE_ID}).find_all("tr")  # type: ignore
        if len(table_rows) < 3:
            return pd.DataFrame()
        table_rows = table_rows[1:-2]
        cells = [
            [clean_cell_text(cell.text) for cell in row.find_all("td")]
            for row in table_rows
        ]
        table = pd.DataFrame(cells, columns=["date", "value"])
        return table


def extract_page_data(page_html: str) -> pd.DataFrame:
    soup = BeautifulSoup(page_html, "html.parser")
    html_tables = soup.find_all("table", {"class": ["insTable"]})[:6]
    table = pd.DataFrame(
        [
            [clean_cell_text(cell.text) for cell in row.find_all("td")]
            for table in html_tables
            for row in table.find_all("tr")
        ]
    )
    columns_translation = get_metadata("page_columns")
    table[0] = MapTitles(columns_translation).map_titles(table[0].to_list())  # type: ignore
    page_data = table.set_index(0).T
    page_data = page_data.replace("", None)
    return page_data
