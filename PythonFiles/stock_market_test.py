# -*- coding: utf-8 -*-
"""
Author: Travis Campos
Date: 03/21/2019

Spyder Editor

Stock Market
"""
#%%
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import dateutil.relativedelta
import re
import numpy as np





now = dt.datetime.now()

style.use('ggplot')

start = dt.datetime(2016,9,25)
end = dt.datetime(now.year,now.month,now.day)


def find_date(month_count):
    d = dt.datetime.strptime(str(now.year)+"-"+str(now.month)+"-"+str(now.day), "%Y-%m-%d")
    d2 = d - dateutil.relativedelta.relativedelta(months=month_count)
    
    lst = []
    lst = re.split('-',str(d2))
    
    new_lst = []
    new_lst.append(int(lst[0]))
    new_lst.append(int(lst[1]))
    
    info = re.split("\s",lst[2])

    
    new_lst.append(int(info[0]))
    return new_lst


global_df = web.DataReader('AAPL','yahoo',start,end)
global_df.to_csv('stock.csv')




global_df = pd.read_csv('stock.csv',parse_dates = True, index_col = 0)
global_df['50ma'] = global_df['Adj Close'].rolling(window = 50,min_periods = 0).mean()
global_df['100ma'] = global_df['Adj Close'].rolling(window = 100,min_periods = 0).mean()
global_df['200ma'] = global_df['Adj Close'].rolling(window = 200,min_periods = 0).mean()



#ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
#ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1) 



ax1 = plt.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
ax1.get_xaxis().set_ticks([])
plt.ylabel("Stock Price")
    


ax0 = plt.subplot2grid((6,4), (0,0), rowspan=1, colspan=4)
ax0.get_xaxis().set_ticks([])
ax0.set_yticks([30,70])
plt.ylabel("RSI")

plt.title("Stock Market Technical Indicator Graph")

ax2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4)
ax2.set_yticks([-100,100])

plt.ylabel("MACD")



def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array


def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow=26, fast=12):
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow

def plot():
    
    plt.rcParams["figure.figsize"] = (10,5)
    ax1.plot(global_df.index, global_df['Adj Close'],color = 'Green')
    ax1.plot(global_df.index, global_df['50ma'], color = 'Purple', label = "50 DMA")
    ax1.plot(global_df.index, global_df['100ma'], color = 'Blue',label = "100 DMA")
    ax1.plot(global_df.index, global_df['200ma'], color = 'Red',label = "200 DMA")

    handles, labels = ax1.get_legend_handles_labels()
    
    del handles[0]
    del labels[0]

    ax1.legend(handles, labels, loc = 2)
    
    ax2.bar(global_df.index, global_df['Volume']/1000000)
    

    
    plt.show()
    '''
    MA1 = 10
    MA2 = 50
    
    Av1 = movingaverage(closep, MA1)
    Av2 = movingaverage(closep, MA2)

    SP = len(date[MA2-1:])
    ax0.plot(date[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
    ax0.axhline(70, color=negCol)
    ax0.axhline(30, color=posCol)
    ax0.fill_between(date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol, alpha=0.5)
    ax0.fill_between(date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol, alpha=0.5)
    ax0.set_yticks([30,70])
        
        
    
    plt.savefig('new_chart.png')
    '''
    return

plot()


#%%