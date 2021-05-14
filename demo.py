import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from matplotlib import gridspec
import mpl_finance as mpf
import talib




'''
def draw_k_Line(df,method="CDLDOJISTAR"):
    mytalib=talib
    f=getattr(mytalib,method)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    mpf.candlestick2_ochl(ax, df["open"], df["close"], df["high"], df["low"], width=0.6, colorup='r',
                          colordown='green',
                          alpha=1.0)
    df['star'] = f(df['open'].values, df['high'].values, df['low'].values, df['close'].values)

    pattern = df[(df['star'] == 100) | (df['star'] == -100)]
    for key, val in df.items():
        for index, today in pattern.iterrows():
            x_posit = df.index.get_loc(index)
            ax.annotate("{}\n{}".format("十字星", today["date"]), xy=(x_posit, today["high"]),
                        xytext=(0, pattern["close"].mean()), xycoords="data",
                        fontsize=8, textcoords="offset points", arrowprops=dict(arrowstyle="simple", color="r"))

    ax.xaxis.set_major_locator(ticker.MaxNLocator(9))

    def format_date(x, pos=None):
        if x < 0 or x > len(df['date']) - 1:
            return ''
        return df['date'][int(x)]

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax.grid(True)
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.show()

df = pd.read_excel("海尔智家k.xlsx")
df['date'] = pd.to_datetime(df['date'])
df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
draw_k_Line(df)

df = pd.read_excel("sh600690.xlsx")
df['成交时间'] = pd.to_datetime(df['成交时间'])
df['成交时间'] = df['成交时间'].apply(lambda x: x.strftime('%H:%M'))
fig= plt.figure()
spec = gridspec.GridSpec(2,1,height_ratios=[2,1])
ax1 = fig.add_subplot(spec[0])
ax2 = fig.add_subplot(spec[1])
plt.rcParams['font.sans-serif'] = ['SimHei']
ax1.plot(np.arange(0, len(df["成交时间"])), df["成交价格"], color='black')

ax1.xaxis.set_major_locator(ticker.MaxNLocator(3))

df_buy = np.where(df["性质"] == "买盘", df["成交量(手)"], 0)
df_sell = np.where(df["性质"] == "卖盘", df["成交量(手)"], 0)

ax2.bar(np.arange(0, len(df)), df_buy, color="red")
ax2.bar(np.arange(0, len(df)), df_sell, color="blue")
ax2.set_ylim([0,df["成交量(手)"].max()])

def format_date(x, pos=None):
    if x < 0 or x > len(df['成交时间']) - 1:
        return ''
    return df['成交时间'][int(x)]


ax1.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
ax1.grid(True)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.show()
'''
