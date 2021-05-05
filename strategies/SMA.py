import backtrader as bt
import math
import pandas as pd
import numpy as np

class PandasSMA(bt.feeds.PandasData):
    lines = ('sma30','sma100','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',2),
        ('low',3),
        ('close',4),
        ('volume',6),
        ('openinterest',None),
        ('adj_close',5),
        ('sma30', 7),
        ('sma100', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )

class TestSMA(bt.Strategy):
    def __init__(self):
        self.sell_signal = self.datas[0].sell_signal
        self.buy_signal = self.datas[0].buy_signal

    def next(self):
        if not(math.isnan(self.buy_signal[0])):
            self.buy()
            print('buy at',self.buy_signal[0])
        elif not(math.isnan(self.sell_signal[0])):
            self.sell()
            print('sell at',self.sell_signal[0])


# Create a function to signal when to buy and when to sell the asset/stock
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['Adj Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Adj Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy, sigPriceSell)


def run_SMA(df):
    # Create the simple moving average with a 30 day window (30 MA)
    SMA30 = pd.DataFrame()
    SMA30['Adj Close Price'] = df['Adj Close'].rolling(window=30).mean()

    # Create the simple moving 100 day average (100 MA)

    SMA100 = pd.DataFrame()
    SMA100['Adj Close Price'] = df['Adj Close'].rolling(window=100).mean()

    # save sma30/sma100 into df
    df['SMA30'] = SMA30['Adj Close Price']
    df['SMA100'] = SMA100['Adj Close Price']

    # Store the buy and sell data into a variable
    buy_sell1 = buy_sell(df)
    df['Buy_Signal_Price'] = buy_sell1[0]
    df['Sell_Signal_Price'] = buy_sell1[1]



