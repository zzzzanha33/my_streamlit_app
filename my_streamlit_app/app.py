"""実行用のファイル"""

from structure_for_synthesis import XRepository as REPO
from excel_arranger import ExcelArranger as Ex
from ui import UI

if __name__ == "__main__":
    ex = Ex()
    repo = REPO()

    repo = ex.excel_register(repo)

    ui = UI(repo)

    ui.run()
