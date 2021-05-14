import talib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mpl_finance as mpf
from matplotlib import gridspec


class KMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        spec = gridspec.GridSpec(4, 1, height_ratios=[3, 1, 1, 1])
        self.ax1 = self.fig.add_subplot(spec[0])
        self.ax2 = self.fig.add_subplot(spec[1])
        self.ax3 = self.fig.add_subplot(spec[2])
        self.ax4 = self.fig.add_subplot(spec[3])
        self.setParent(parent)
        self.k_text = ['十字星', '两只乌鸦', '三只乌鸦', '三内部上涨和下跌', '三线打击',
                       '三外部上涨和下跌', '南方三星', '三个白兵', '弃婴', '大敌当前',
                       '捉腰带线', '脱离', '收盘缺影线', '藏婴吞没', '反击线'
            , '乌云压顶', '蜻蜓十字/T形十字', '吞噬模式', '十字暮星', '暮星',
                       '向上/下跳空并列阳线', '墓碑十字/倒T十字', '锤头', '上吊线', '母子线',
                       '十字孕线', '风高浪大线', '陷阱', '修正陷阱', '家鸽',
                       '三胞胎乌鸦', '颈内线', '倒锤头', '反冲形态', '由较长缺影线决定的反冲形态',
                       '停顿形态', '条形三明治', '探水竿', '跳空并列阴阳线', '插入',
                       '三星', '奇特三河床', '向上跳空的两只乌鸦', '上升/下降跳空三法']

        FigureCanvas.updateGeometry(self)

    def start_staict_plot(self, df, method="CDLDOJISTAR", numb=0):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        self.fig.canvas.draw_idle()
        mytalib = talib
        f = getattr(mytalib, method)
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        mpf.candlestick2_ochl(self.ax1, df["open"], df["close"], df["high"], df["low"], width=0.6, colorup='r',
                              colordown='green',
                              alpha=1.0)
        df['star'] = f(df['open'].values, df['high'].values, df['low'].values, df['close'].values)

        pattern = df[(df['star'] == 100) | (df['star'] == -100)]
        for key, val in df.items():
            for index, today in pattern.iterrows():
                x_posit = df.index.get_loc(index)
                self.ax1.annotate("{}\n{}".format(self.k_text[numb], today["date"]), xy=(x_posit, today["high"]),
                                  xytext=(0, pattern["close"].mean()), xycoords="data",
                                  fontsize=8, textcoords="offset points",
                                  arrowprops=dict(arrowstyle="simple", color="r"))
        df["SMA5"] = df["close"].rolling(5).mean()
        df["SMA10"] = df["close"].rolling(10).mean()
        df["SMA30"] = df["close"].rolling(30).mean()
        df["SMA60"] = df["close"].rolling(60).mean()
        self.ax1.plot(np.arange(0, len(df)), df['SMA5'], label="5日均线")  # 绘制5日均线
        self.ax1.plot(np.arange(0, len(df)), df['SMA10'], label="10日均线")  # 绘制10日均线
        self.ax1.plot(np.arange(0, len(df)), df['SMA30'], label="30日均线")  # 绘制30日均线
        self.ax1.plot(np.arange(0, len(df)), df['SMA60'], label="60日均线")  # 绘制30日均线
        self.ax1.legend()

        red_pred = np.where(df["close"] > df["open"], df["volume"], 0)
        blue_pred = np.where(df["close"] < df["open"], df["volume"], 0)
        self.ax2.bar(np.arange(0, len(df)), red_pred, facecolor="red")
        self.ax2.bar(np.arange(0, len(df)), blue_pred, facecolor="blue")
        self.ax2.set(ylabel=u"成交量")

        low_list = df["close"].rolling(9, min_periods=1).min()
        high_list = df["high"].rolling(9, min_periods=1).max()
        rsv = (df["close"] - low_list) / (high_list - low_list) * 100
        df["K"] = rsv.ewm(com=2, adjust=False).mean()
        df["D"] = df["K"].ewm(com=2, adjust=False).mean()
        df["J"] = 3 * df["K"] - 2 * df["D"]
        self.ax3.plot(df["date"], df["K"], label="K")
        self.ax3.plot(df["date"], df["D"], label="D")
        self.ax3.plot(df["date"], df["J"], label="J")
        self.ax3.legend()
        self.ax3.set(ylabel=u"KDJ")

        EMA1 = df["close"].ewm(span=12, adjust=False).mean()
        EMA2 = df["close"].ewm(span=26, adjust=False).mean()
        DIF = EMA1 - EMA2
        DEA = DIF.ewm(span=9, adjust=False).mean()
        BAR = 2 * (DIF - DEA)

        red_bar = np.where(BAR > 0, BAR, 0)
        blue_bar = np.where(BAR < 0, BAR, 0)

        self.ax4.plot(np.arange(0, len(df)), DIF)
        self.ax4.plot(np.arange(0, len(df)), DEA)

        self.ax4.bar(np.arange(0, len(df)), red_bar, color="red")
        self.ax4.bar(np.arange(0, len(df)), blue_bar, color="blue")
        self.ax4.set(ylabel=u"MACD")
        self.ax1.xaxis.set_major_locator(ticker.MaxNLocator(9))

        def format_date(x, pos=None):
            if x < 0 or x > len(df['date']) - 1:
                return ''
            return df['date'][int(x)]

        self.ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        self.ax1.grid(True)
        plt.setp(self.ax1.get_xticklabels(), visible=True)
        plt.setp(self.ax2.get_xticklabels(), visible=False)
        plt.setp(self.ax3.get_xticklabels(), visible=False)
        plt.setp(self.ax4.get_xticklabels(), visible=False)
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
