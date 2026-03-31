"""エクセルから読み込む"""

from pathlib import Path
import openpyxl

from src.models.base import XRepository as REPO, Synthesis, Catalyst, Progress


class ExcelArranger:
    """ブック・シートの取得"""

    def __init__(self):
        self.book: openpyxl.Workbook
        self.sheet = None

    def al_book(self):
        base_dir = Path(__file__).resolve()
        file_path = base_dir.parent.parent.joinpath("data", "合成表.xlsx")
        self.open_book(file_path)

    def open_book(self, file_path):
        self.book = openpyxl.load_workbook(filename=file_path)
        self.sheet = self.book["Sheet1"]

    def input_row(self):
        list_row = [row for row in self.sheet.iter_rows(min_row=2, values_only=True)]
        return list_row

    def tuple_to_register(self, row: tuple[str, ...]):
        y, c, h, *xs = row
        list_x = [x for x in xs if x is not None]
        return y, c, h, list_x

    def excel_register(self, repo: REPO):
        rows = self.input_row()
        for row in rows:
            y_name, catalyst, habitat, list_x = self.tuple_to_register(row)
            repo = repo.register_x(y_name)
            for x_name in list_x:
                repo.register_x(x_name)
            synthesis = Synthesis(
                repo[y_name],
                Catalyst.from_str(catalyst),
                *[repo[x_name] for x_name in list_x],
            )
            repo = repo.register_synthesis(synthesis)
            if list_x == []:
                repo = repo.register_habitat(y_name, Progress.from_str(habitat))
        return repo
