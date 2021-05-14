import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from matplotlib import gridspec
class StockMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        spec = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
        self.ax1 = self.fig.add_subplot(spec[0])
        self.ax2 = self.fig.add_subplot(spec[1])
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)


    def start_staict_plot(self, df):
        df['成交时间'] = pd.to_datetime(df['成交时间'])
        df['成交时间'] = df['成交时间'].apply(lambda x: x.strftime('%H:%M'))
        self.ax1.plot(np.arange(0, len(df["成交时间"])), df["成交价格"], color='black')
        df_buy = np.where(df["性质"] == "买盘", df["成交量(手)"], 0)
        df_sell = np.where(df["性质"] == "卖盘", df["成交量(手)"], 0)
        self.ax1.set(ylabel=u"股价走势图")
        self.ax2.bar(np.arange(0, len(df)), df_buy, color="red")
        self.ax2.bar(np.arange(0, len(df)), df_sell, color="blue")
        self.ax2.set_ylim([0, df["成交量(手)"].max()/3])
        self.ax2.set(ylabel=u"成交量分时图")
        self.ax1.xaxis.set_major_locator(ticker.MaxNLocator(3))

        def format_date(x, pos=None):
            if x < 0 or x > len(df['成交时间']) - 1:
                return ''
            return df['成交时间'][int(x)]

        self.ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        self.ax1.grid(True)
        plt.setp(self.ax2.get_xticklabels(), visible=False)
        plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
