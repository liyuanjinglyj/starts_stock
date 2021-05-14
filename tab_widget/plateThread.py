import time

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import requests

#板块指数详细数据线程
class plateThread(QtCore.QThread):
    _signal = pyqtSignal(list)

    def __init__(self):
        super(plateThread, self).__init__()

    def run(self):
        list = []
        qListName = ['s_sh000001', 's_sz399001', 's_sz399006', 's_sh000688', 's_sh000016', 's_sh000905',
                     's_sh000300', ]  # 添加的数组数据
        while True:
            list.clear()
            baseUrl = 'http://hq.sinajs.cn/list='
            for index in qListName:
                url = baseUrl + index
                temp = requests.get(url).text
                list.append(temp)
            self._signal.emit(list)
            time.sleep(10)
