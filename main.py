import sys
import qdarkstyle
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from k_tab.kLineThread import KLineThread
from k_tab.k_line_pic import KMplCanvas
from nch_tab.nchThread import NchThread
from other_tab.otherThread import OtherThread
from tab_widget.mianThread import MainPlotThread
from tab_widget.plateThread import plateThread
from tab_widget.shareThread import ShareThread
from tab_widget.stock_day_pic import StockMplCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar


class MyFrom(QMainWindow):
    def __init__(self, parent=None):
        super(MyFrom, self).__init__(parent=parent)
        self.setWindowTitle('星辰股票行情软件')
        self.resize(1100, 700)
        self.isListView = True
        self.init()

    def init(self):
        self.qTableWidget = QTabWidget()
        self.homeTab = QWidget()
        self.kTab2 = QWidget()
        self.otherTab = QWidget()
        self.nchTab = QWidget()
        self.qTableWidget.addTab(self.homeTab, "主页")
        self.qTableWidget.addTab(self.kTab2, "K线图")
        self.qTableWidget.addTab(self.otherTab, "龙虎榜")
        self.qTableWidget.addTab(self.nchTab, "北向资金")

        self.init_hometab()
        self.init_kTab()
        self.init_otherTab()
        self.init_nch()
        self.setCentralWidget(self.qTableWidget)


    # 北向资金
    def init_nch(self):
        self.nchGrid = QGridLayout()
        self.nchGrid.setSpacing(5)
        self.nchTab.setLayout(self.nchGrid)
        self.nchThread = NchThread()
        self.nchThread._signal.connect(self.nchThead_callbacklog)
        self.nchThread.start()

    def nchThead_callbacklog(self, df):
        ft = QFont()
        ft.setPointSize(10)
        ft.setBold(True)
        nchtableWidget = QTableWidget(len(df), 6)
        nchtableWidget.setHorizontalHeaderLabels(
            ['名称', '最新涨跌幅', '北向资金今日持股-股票只数', "北向资金今日增持估计-市值", "今日增持最大股-市值", "今日减持最大股-市值"])
        nchtableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        nchtableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 禁止拖拽
        nchtableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 只能选中一行
        nchtableWidget.itemClicked.connect(self.tableWidget_connect)
        nchtableWidget.verticalHeader().setVisible(False)
        nchtableWidget.setShowGrid(False)  # 不显示子线条
        nchtableWidget.setColumnWidth(0, 150)  # 设置第一列宽
        nchtableWidget.setColumnWidth(1, 100)  # 设置第二列宽
        nchtableWidget.setColumnWidth(2, 200)  # 设置第三列宽
        nchtableWidget.setColumnWidth(3, 210)  # 设置第三列宽
        nchtableWidget.setColumnWidth(4, 200)  # 设置第三列宽
        nchtableWidget.setColumnWidth(5, 200)  # 设置第三列宽
        for idx, row in df.iterrows():
            if float(row["最新涨跌幅"]) < 0:
                m_color = QColor(0, 255, 0)
            elif float(row["最新涨跌幅"]) > 0:
                m_color = QColor(255, 0, 0)
            else:
                m_color = QColor(255, 255, 255)
            newItem0 = QTableWidgetItem(str(row["名称"]))
            newItem0.setFont(ft)
            newItem0.setForeground(QBrush(m_color))
            newItem1 = QTableWidgetItem(str(row["最新涨跌幅"]))
            newItem1.setFont(ft)
            newItem1.setForeground(QBrush(m_color))
            newItem2 = QTableWidgetItem(str(row["北向资金今日持股-股票只数"]))
            newItem2.setFont(ft)
            newItem2.setForeground(QBrush(m_color))
            newItem3 = QTableWidgetItem(str(row["北向资金今日增持估计-市值"]))
            newItem3.setFont(ft)
            newItem3.setForeground(QBrush(m_color))
            newItem4 = QTableWidgetItem(str(row["今日增持最大股-市值"]))
            newItem4.setFont(ft)
            newItem4.setForeground(QBrush(m_color))
            newItem5 = QTableWidgetItem(str(row["今日减持最大股-市值"]))
            newItem5.setFont(ft)
            newItem5.setForeground(QBrush(m_color))
            newItem0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem4.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            newItem5.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            nchtableWidget.setItem(idx, 0, newItem0)
            nchtableWidget.setItem(idx, 1, newItem1)
            nchtableWidget.setItem(idx, 2, newItem2)
            nchtableWidget.setItem(idx, 3, newItem3)
            nchtableWidget.setItem(idx, 4, newItem4)
            nchtableWidget.setItem(idx, 5, newItem5)
        self.nchGrid.addWidget(nchtableWidget, 0, 0, 16, 16)

    # 龙虎榜
    def init_otherTab(self):
        self.otherGrid = QGridLayout()
        self.otherGrid.setSpacing(5)
        ft = QFont()
        ft.setPointSize(26)
        ft.setBold(True)
        rise_label = QLabel("涨幅偏离值达7%的股票")
        rise_label.setFont(ft)
        rise_label.setStyleSheet("color:red")
        fall_label = QLabel("跌幅偏离值达7%的股票")
        fall_label.setFont(ft)
        self.otherGrid.addWidget(rise_label, 0, 0, 1, 8)
        self.otherGrid.addWidget(fall_label, 0, 8, 1, 8)
        self.otherTab.setLayout(self.otherGrid)
        self.otherThread = OtherThread()
        self.otherThread._signalRise.connect(self.otherRise_callbacklog)
        self.otherThread._signalFall.connect(self.otherFall_callbacklog)
        self.otherThread.start()

    def otherFall_callbacklog(self, df):
        ft = QFont()
        ft.setPointSize(10)
        ft.setBold(True)
        m_color = QColor(0, 255, 0)
        otherFalltableWidget = QTableWidget(len(df), 6)
        otherFalltableWidget.setHorizontalHeaderLabels(['股票名称', '股票代码', '收盘价', "对应值", "成交量", "成交额"])
        otherFalltableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        otherFalltableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 禁止拖拽
        otherFalltableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 只能选中一行
        otherFalltableWidget.itemClicked.connect(self.tableWidget_connect)
        otherFalltableWidget.verticalHeader().setVisible(False)
        otherFalltableWidget.setShowGrid(False)  # 不显示子线条
        otherFalltableWidget.setColumnWidth(0, 70)  # 设置第一列宽
        otherFalltableWidget.setColumnWidth(1, 70)  # 设置第二列宽
        otherFalltableWidget.setColumnWidth(2, 70)  # 设置第三列宽
        otherFalltableWidget.setColumnWidth(3, 70)  # 设置第三列宽
        otherFalltableWidget.setColumnWidth(4, 120)  # 设置第三列宽
        otherFalltableWidget.setColumnWidth(5, 120)  # 设置第三列宽
        for idx, row in df.iterrows():
            newItem0 = QTableWidgetItem(str(row["股票名称"]))
            newItem0.setFont(ft)
            newItem0.setForeground(QBrush(m_color))
            newItem1 = QTableWidgetItem(str(row["股票代码"]))
            newItem1.setFont(ft)
            newItem1.setForeground(QBrush(m_color))
            newItem2 = QTableWidgetItem(str(row["收盘价"]))
            newItem2.setFont(ft)
            newItem2.setForeground(QBrush(m_color))
            newItem3 = QTableWidgetItem(str(row["对应值"]))
            newItem3.setFont(ft)
            newItem3.setForeground(QBrush(m_color))
            newItem4 = QTableWidgetItem(str(row["成交量"]))
            newItem4.setFont(ft)
            newItem4.setForeground(QBrush(m_color))
            newItem5 = QTableWidgetItem(str(row["成交额"]))
            newItem5.setFont(ft)
            newItem5.setForeground(QBrush(m_color))
            otherFalltableWidget.setItem(idx, 0, newItem0)
            otherFalltableWidget.setItem(idx, 1, newItem1)
            otherFalltableWidget.setItem(idx, 2, newItem2)
            otherFalltableWidget.setItem(idx, 3, newItem3)
            otherFalltableWidget.setItem(idx, 4, newItem4)
            otherFalltableWidget.setItem(idx, 5, newItem5)
        self.otherGrid.addWidget(otherFalltableWidget, 1, 8, 10, 8)

    def otherRise_callbacklog(self, df):
        ft = QFont()
        ft.setPointSize(10)
        ft.setBold(True)
        m_color = QColor(255, 0, 0)
        otherRisetableWidget = QTableWidget(len(df), 6)
        otherRisetableWidget.setHorizontalHeaderLabels(['股票名称', '股票代码', '收盘价', "对应值", "成交量", "成交额"])
        otherRisetableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
        otherRisetableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 禁止拖拽
        otherRisetableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 只能选中一行
        otherRisetableWidget.itemClicked.connect(self.tableWidget_connect)
        otherRisetableWidget.verticalHeader().setVisible(False)
        otherRisetableWidget.setShowGrid(False)  # 不显示子线条
        otherRisetableWidget.setColumnWidth(0, 70)  # 设置第一列宽
        otherRisetableWidget.setColumnWidth(1, 70)  # 设置第二列宽
        otherRisetableWidget.setColumnWidth(2, 70)  # 设置第三列宽
        otherRisetableWidget.setColumnWidth(3, 70)  # 设置第三列宽
        otherRisetableWidget.setColumnWidth(4, 120)  # 设置第三列宽
        otherRisetableWidget.setColumnWidth(5, 120)  # 设置第三列宽
        for idx, row in df.iterrows():
            newItem0 = QTableWidgetItem(str(row["股票名称"]))
            newItem0.setFont(ft)
            newItem0.setForeground(QBrush(m_color))
            newItem1 = QTableWidgetItem(str(row["股票代码"]))
            newItem1.setFont(ft)
            newItem1.setForeground(QBrush(m_color))
            newItem2 = QTableWidgetItem(str(row["收盘价"]))
            newItem2.setFont(ft)
            newItem2.setForeground(QBrush(m_color))
            newItem3 = QTableWidgetItem(str(row["对应值"]))
            newItem3.setFont(ft)
            newItem3.setForeground(QBrush(m_color))
            newItem4 = QTableWidgetItem(str(row["成交量"]))
            newItem4.setFont(ft)
            newItem4.setForeground(QBrush(m_color))
            newItem5 = QTableWidgetItem(str(row["成交额"]))
            newItem5.setFont(ft)
            newItem5.setForeground(QBrush(m_color))
            otherRisetableWidget.setItem(idx, 0, newItem0)
            otherRisetableWidget.setItem(idx, 1, newItem1)
            otherRisetableWidget.setItem(idx, 2, newItem2)
            otherRisetableWidget.setItem(idx, 3, newItem3)
            otherRisetableWidget.setItem(idx, 4, newItem4)
            otherRisetableWidget.setItem(idx, 5, newItem5)
        self.otherGrid.addWidget(otherRisetableWidget, 1, 0, 10, 8)

    # K线模块
    def init_kTab(self):
        self.grid_k = QGridLayout()
        self.grid_k.setSpacing(5)
        k_text = ['十字星', '两只乌鸦', '三只乌鸦', '三内部上涨和下跌', '三线打击',
                  '三外部上涨和下跌', '南方三星', '三个白兵', '弃婴', '大敌当前',
                  '捉腰带线', '脱离', '收盘缺影线', '藏婴吞没', '反击线'
            , '乌云压顶', '蜻蜓十字/T形十字', '吞噬模式', '十字暮星', '暮星',
                  '向上/下跳空并列阳线', '墓碑十字/倒T十字', '锤头', '上吊线', '母子线',
                  '十字孕线', '风高浪大线', '陷阱', '修正陷阱', '家鸽',
                  '三胞胎乌鸦', '颈内线', '倒锤头', '反冲形态', '由较长缺影线决定的反冲形态',
                  '停顿形态', '条形三明治', '探水竿', '跳空并列阴阳线', '插入',
                  '三星', '奇特三河床', '向上跳空的两只乌鸦', '上升/下降跳空三法']
        self.k_content = ['预示着当前趋势反转', '预示股价下跌', '预示股价下跌', '预示着股价上涨', '预示股价下跌',
                          '预示着股价上涨', '预示下跌趋势反转，股价上升', '预示股价上升', '预示趋势反转，发生在顶部下跌，底部上涨', '预示股价下跌'
            , '收盘价接近最高价，预示价格上涨', '预示价格上涨', '预示着趋势持续', '预示着底部反转', '预示趋势反转'
            , '预示着股价下跌', '预示趋势反转', '预示趋势反转', '预示顶部反转', '预示顶部反转',
                          '趋势持续', '预示底部反转', '处于下跌趋势底部,预示反转', '处于上升趋势的顶部，预示着趋势反转', '预示趋势反转，股价上升',
                          '预示着趋势反转', '预示着趋势反转', '趋势继续', '趋势继续', '预示着趋势反转',
                          '预示价格下跌', '预示着下跌继续', '在下跌趋势底部，预示着趋势反转', '存在跳空缺口', '与反冲形态类似，较长缺影线决定价格的涨跌',
                          '预示着上涨结束', '预示着股价上涨', '预示趋势反转', '上升趋势持续', '预示着趋势持续',
                          '预示着趋势反转', '收盘价不高于第二日收盘价，预示着反转，第二日下影线越长可能性越大', '预示股价下跌', '收盘价高于第一日收盘价，预示股价上升']
        self.K_method = ['CDLDOJISTAR', 'CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE',
                         'CDL3OUTSIDE', 'CDL3STARSINSOUTH', 'CDL3WHITESOLDIERS', 'CDLABANDONEDBABY', 'CDLADVANCEBLOCK',
                         'CDLBELTHOLD', 'CDLBREAKAWAY', 'CDLCLOSINGMARUBOZU', 'CDLCONCEALBABYSWALL', 'CDLCOUNTERATTACK',
                         'CDLDARKCLOUDCOVER', 'CDLDRAGONFLYDOJI', 'CDLENGULFING', 'CDLEVENINGDOJISTAR',
                         'CDLEVENINGSTAR',
                         'CDLGAPSIDESIDEWHITE', 'CDLGRAVESTONEDOJI', 'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI',
                         'CDLHARAMICROSS', 'CDLHIGHWAVE', 'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON',
                         'CDLIDENTICAL3CROWS', 'CDLINNECK', 'CDLINVERTEDHAMMER', 'CDLKICKING', 'CDLKICKINGBYLENGTH',
                         'CDLSTALLEDPATTERN', 'CDLSTICKSANDWICH', 'CDLTAKURI', 'CDLTASUKIGAP', 'CDLTHRUSTING',
                         'CDLTRISTAR', 'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS', 'CDLXSIDEGAP3METHODS']
        self.cb = QComboBox()
        self.cb.addItems(k_text)
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.cb_label = QLabel("预示着当前趋势反转")
        self.k_label = QLabel("选择K线图的形态：")
        self.grid_k.addWidget(self.k_label, 0, 0, 1, 1)
        self.grid_k.addWidget(self.cb, 0, 2, 1, 2)
        self.grid_k.addWidget(self.cb_label, 0, 5, 1, 5)
        self.kTab2.setLayout(self.grid_k)
        self.kLineThread = KLineThread()
        self.kLineThread.setValue("sh600690")
        self.kLineThread._signal.connect(self.kLineThread_callbacklog)
        self.kLineThread.start()

    def kLineThread_callbacklog(self, df):
        self.df = df
        self.mplK = KMplCanvas(self, width=5, height=4, dpi=100)
        self.mplK.start_staict_plot(df)
        mpl_ntb = NavigationToolbar(self.mplK, self)
        mpl_ntb.setStyleSheet("background-color:white;color:black")

        self.grid_k.addWidget(self.mplK, 2, 0, 13, 12)
        self.grid_k.addWidget(mpl_ntb, 2, 0, 1, 5)

    def selectionchange(self, i):
        self.cb_label.setText(self.k_content[i])
        self.mplK.start_staict_plot(self.df, self.K_method[i], i)

    # 主页模块
    def init_hometab(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        ft = QFont()
        ft.setPointSize(26)
        ft.setBold(True)
        self.share_params = [QLabel() for x in range(10)]
        self.grid.addWidget(self.share_params[0], 0, 0, 2, 3)
        self.share_params[0].setFont(ft)
        self.share_params[0].setStyleSheet("color:yellow")
        self.grid.addWidget(self.share_params[1], 0, 3, 1, 2)
        self.share_params[1].setFont(ft)
        self.grid.addWidget(self.share_params[2], 0, 5)
        self.grid.addWidget(self.share_params[3], 0, 6)
        self.grid.addWidget(self.share_params[4], 0, 7)
        self.grid.addWidget(self.share_params[5], 1, 3)
        self.grid.addWidget(self.share_params[6], 1, 4)
        self.grid.addWidget(self.share_params[7], 1, 5)
        self.grid.addWidget(self.share_params[8], 1, 6)
        self.grid.addWidget(self.share_params[9], 1, 7)
        self.shareThread = ShareThread()
        self.shareThread.setValue("sh600690")
        self.shareThread._signal.connect(self.shareThread_callbacklog)
        self.shareThread.start()

        self.qListOne = ['上证指数', '深证成指', '创业板指', '科创50', '上证50', '中证500', '沪深300']  # 添加的数组数据
        self.plateThread = plateThread()
        self.plateThread._signal.connect(self.plateThread_callbacklog)
        self.plateThread.start()
        self.homeTab.setLayout(self.grid)

        self.mainThread = MainPlotThread()
        self.mainThread.setValue("sh600690")
        self.mainThread._signal.connect(self.mianThread_callbacklog)
        self.mainThread._orderList.connect(self.orderThread_callbacklog)
        self.mainThread.start()

    def mianThread_callbacklog(self, df):
        mpl = StockMplCanvas(self, width=5, height=4, dpi=100)
        mpl.start_staict_plot(df)
        mpl_ntb = NavigationToolbar(mpl, self)
        mpl_ntb.setStyleSheet("background-color:white;color:black")

        self.grid.addWidget(mpl, 2, 0, 12, 12)
        self.grid.addWidget(mpl_ntb, 2, 0, 1, 5)

    def shareThread_callbacklog(self, shareList):
        isloss = float(shareList[5])
        i = 0
        for share_label, qlist in zip(self.share_params, shareList):
            if i == 1:
                share_label.setText(str(qlist))
                if isloss >= 0:
                    share_label.setStyleSheet("color:red")
                else:
                    share_label.setStyleSheet("color:rgb(0, 255, 0)")
            else:
                share_label.setText(str(qlist))
            i += 1

    def plateThread_callbacklog(self, urlList):
        i = 0
        one_QLabel = [QLabel() for x in range(7)]
        two_QLabel = [QLabel() for x in range(7)]
        for o_label, t_label, qlist, m_name in zip(one_QLabel, two_QLabel, urlList, self.qListOne):
            temp = qlist.split('"')[1].split(',')
            isloss = float(str(round(float(temp[2]), 2)))
            if isloss >= 0:
                o_label.setStyleSheet("color:red;font-size:14px")
                t_label.setStyleSheet("color:red;font-size:14px")
            else:
                o_label.setStyleSheet("color:rgb(0, 255, 0);font-size:14px")
                t_label.setStyleSheet("color:rgb(0, 255, 0);font-size:14px")
            o_label.setText(m_name)
            self.grid.addWidget(o_label, 0, 8 + i, 1, 1)
            t_label.setText(str(round(float(temp[1]), 2)))
            self.grid.addWidget(t_label, 1, 8 + i, 1, 1)
            i += 1

    # 指数显示模块
    def tableWidget_connect(self, item):
        QMessageBox.information(self, "QTableWidget", "你选择了" + item.text())

    def orderThread_callbacklog(self, urlList):
        ft = QFont()
        ft.setPointSize(10)
        ft.setBold(True)
        m_color = None
        j = 0
        if not self.isListView:
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['性质', '成交量(手)', '成交额(元)'])
            for qlist in urlList:
                for index, m_dict in enumerate(qlist):
                    if index == 0:
                        if str(m_dict).strip() == "买盘":
                            m_color = QColor(255, 0, 0)
                        elif str(m_dict).strip() == "卖盘":
                            m_color = QColor(0, 255, 0)
                        else:
                            m_color = QColor(255, 255, 255)
                    newItem = QTableWidgetItem(str(m_dict))
                    newItem.setFont(ft)
                    newItem.setForeground(QBrush(m_color))
                    self.tableWidget.setItem(j, index, newItem)
                j += 1
        else:
            # 各个板块指数
            self.tableWidget = QTableWidget(len(urlList), 3)
            self.tableWidget.setHorizontalHeaderLabels(['性质', '成交量(手)', '成交额(元)'])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 禁止拖拽
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 只能选中一行
            self.tableWidget.itemClicked.connect(self.tableWidget_connect)
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.setShowGrid(False)  # 不显示子线条
            self.tableWidget.setColumnWidth(0, 70)  # 设置第一列宽
            self.tableWidget.setColumnWidth(1, 70)  # 设置第二列宽
            self.tableWidget.setColumnWidth(2, 70)  # 设置第三列宽
            for qlist in urlList:
                for index, m_dict in enumerate(qlist):
                    if index == 0:
                        if str(m_dict).strip() == "买盘":
                            m_color = QColor(255, 0, 0)
                        elif str(m_dict).strip() == "卖盘":
                            m_color = QColor(0, 255, 0)
                        else:
                            m_color = QColor(255, 255, 255)
                    newItem = QTableWidgetItem(str(m_dict))
                    newItem.setFont(ft)
                    newItem.setForeground(QBrush(m_color))
                    self.tableWidget.setItem(j, index, newItem)
                j += 1
            self.grid.addWidget(self.tableWidget, 2, 12, 12, 4)
            self.isListView = False
        self.tableWidget.scrollToBottom()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myUI = MyFrom()
    myUI.setWindowFlag(Qt.WindowMinimizeButtonHint)  # 禁止放大界面
    myUI.setFixedSize(myUI.width(), myUI.height())  # 静止拖拽放大界面
    myUI.show()
    sys.exit(app.exec_())
