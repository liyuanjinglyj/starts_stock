import akshare as ak
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from pandas import DataFrame

class NchThread(QtCore.QThread):
    _signal = pyqtSignal(DataFrame)
    def __init__(self):
        super(NchThread, self).__init__()

    def run(self):
        df = ak.stock_em_hsgt_board_rank(symbol="北向资金增持行业板块排行", indicator="今日")
        self._signal.emit(df)