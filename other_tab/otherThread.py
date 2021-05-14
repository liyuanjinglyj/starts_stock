import akshare as ak
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from pandas import DataFrame


class OtherThread(QtCore.QThread):
    _signalRise = pyqtSignal(DataFrame)
    _signalFall = pyqtSignal(DataFrame)

    def __init__(self):
        super(OtherThread, self).__init__()

    def run(self):
        df_rise = ak.stock_sina_lhb_detail_daily(trade_date="20210205", symbol="涨幅偏离值达7%的证券")
        df_fall = ak.stock_sina_lhb_detail_daily(trade_date="20210205", symbol="跌幅偏离值达7%的证券")
        self._signalRise.emit(df_rise)
        self._signalFall.emit(df_fall)
