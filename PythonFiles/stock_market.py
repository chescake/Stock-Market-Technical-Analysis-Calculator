# -*- coding: utf-8 -*-
"""
Author: Travis Campos
Date: 03/21/2019

Spyder Editor

Stock Market
"""
#%%

from datetime import datetime
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
import re

aapl = Stock("MSFT")
info = str(aapl.get_company())
print type(aapl.get_company)

print info

lst = []
lst = re.findall('companyName\': u\'([^\']+)',info)
print lst



    
def test_plot():
    start = datetime(2017, 1, 1)
    end = datetime(2018, 1, 1)
    
    df = get_historical_data("TSLA", start, end)
    
    df = get_historical_data("AAPL", start, end, output_format='pandas')
    
    
    df.plot()
    plt.show()
    
    return


#%%
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


now = dt.datetime.now()

style.use('ggplot')

start = dt.datetime(2014,1,1)
end = dt.datetime(now.year,now.month,now.day)

df = web.DataReader('AAPL','yahoo',start,end)
df.to_csv('stock.csv')




df = pd.read_csv('stock.csv',parse_dates = True, index_col = 0)
df['100ma'] = df['Adj Close'].rolling(window = 100,min_periods = 0).mean()
df['200ma'] = df['Adj Close'].rolling(window = 200,min_periods = 0).mean()


ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1) 

def plot():
    ax1.plot(df.index, df['Adj Close'],color = 'Green')
    ax1.plot(df.index, df['100ma'], color = 'Blue')
    ax1.plot(df.index, df['200ma'], color = 'Red')
    ax2.bar(df.index, df['Volume'])
    plt.savefig('chart.png',)
    return

plot()



#%%