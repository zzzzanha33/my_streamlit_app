"""エクセルから読み込む"""

import openpyxl
import os

from structure_for_synthesis import XRepository as REPO


class ExcelArranger:
    # ブック・シートの取得
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, "合成表.xlsx")

        self.book = openpyxl.load_workbook(filename=file_path)
        self.sheet = self.book["Sheet1"]

    def input_row(self):
        list_row = [row for row in self.sheet.iter_rows(min_row=2, values_only=True)]
        return list_row

    def tuple_to_register(self, row: tuple[str, ...]):
        y, c, *xs = row
        list_x = [x for x in xs if x]
        return y, c, list_x

    def excel_register(self, repo: REPO):
        rows = self.input_row()
        for row in rows:
            name, catalyst, connect_names = self.tuple_to_register(row)
            repo.register(name, catalyst, connect_names)
        return repo
