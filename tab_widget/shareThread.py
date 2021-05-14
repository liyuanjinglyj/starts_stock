import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import requests

from utils import LYJutils

#股票详细数据获取线程
class ShareThread(QtCore.QThread):
    _signal = pyqtSignal(list)

    def __init__(self):
        super(ShareThread, self).__init__()

    def setValue(self, shareNumber):
        self.share_num = shareNumber

    def run(self):
        list = []
        while True:
            list.clear()
            baseUrl = 'http://hq.sinajs.cn/list=' + self.share_num
            temp = requests.get(baseUrl).text.split('"')[1].split(',')
            list.append(temp[0])# 股票的名称
            list.append(round(float(temp[3]), 2))# 当前股票价格
            list.append("高 " + str(round(float(temp[4]), 2)))# 当前股票最高价格
            list.append("开 " + str(round(float(temp[1]), 2)))# 股票开盘价格
            list.append("量比 " + LYJutils.str_of_num(float(temp[8])))# 当前股票量比
            list.append(str(round(float(temp[3]) - float(temp[2]), 2))) # 当前股票涨跌幅
            m_flo = (float(temp[3]) - float(temp[2])) / float(temp[2]) * 100.0
            list.append(str(round(m_flo, 2)) + "%") # 当前股票涨跌幅百分比
            list.append("低 " + str(round(float(temp[5]), 2)))# 当前股票最低价格
            list.append(temp[30])#交易日期
            list.append("金额 " + LYJutils.str_of_num(float(temp[9]))) # 股票成交金额
            self._signal.emit(list)
            time.sleep(10)
