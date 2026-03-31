"""実行用のファイル"""

from src.models.base import XRepository as REPO
from src.infrastructure.excel_handler import ExcelArranger
from src.ui.navigation import Router


class App:
    def __init__(self):
        repo = REPO()
        excelarranger = ExcelArranger()
        excelarranger.al_book()
        repo = excelarranger.excel_register(repo)

        self.router = Router(repo)

    def run(self):
        self.router.run()
