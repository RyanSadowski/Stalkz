import pandas as pd
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas_datareader.data as web
from datetime import datetime


ticker = (sys.argv[1])
print "fetching data for $" + ticker
start = datetime(2016, 1, 1)
end = datetime.now()
df = web.DataReader(ticker, 'yahoo', start, end)
df["20D"] = np.round(df["Close"].rolling(window = 20, center = False).mean(), 2)
df["50D"] = np.round(df["Close"].rolling(window = 50, center = False).mean(), 2)
df["Volume"] = df["Volume"]
df_ohlc = df.reset_index()
df_ohlc=df_ohlc.iloc[50:]


#Naming columns
df_ohlc.columns = ["Date","Open","High",'Low',"Close", "Adj Close", "Volume", "20D", "50D"]
#Converting dates column to float values
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
#Making plot
fig = plt.figure()

ax1 = fig.add_subplot(1,1,1)
# AutoFormat dates
fig.autofmt_xdate()
#Converts raw mdate numbers to dates
ax1.xaxis_date()
plt.xlabel("Date")
ax2 = ax1.twinx()
ax1.set_ylabel('Price')
ax2.set_ylabel('Volume')
ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.2],[0.9,0.32]]))
fig.suptitle('$' + ticker , fontsize=14, fontweight='bold')
#Making candlestick plot
candlestick_ohlc(ax1, df_ohlc.values ,width=1, colorup='g', colordown='k')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax1.grid(True)
#Add the rolling average lines
ax1.plot(df_ohlc['Date'],df_ohlc['20D'],color = 'b')
ax1.plot(df_ohlc['Date'],df_ohlc['50D'],color = 'y')
ax2.plot(df_ohlc['Date'],df_ohlc['Volume'],color='purple')


idx = np.argwhere(np.diff(np.sign(df["20D"] - df["50D"])) != 0).reshape(-1) + 0
ax1.plot(df_ohlc['Date'][idx], df["20D"][idx], 'ro')

ax1.legend()
plt.show()
