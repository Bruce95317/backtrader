import backtrader as bt
import math
import numpy as np

class PandasDEMA(bt.feeds.PandasData):
    lines = ('dema_short','dema_long','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',2),
        ('low',3),
        ('close',4),
        ('volume',6),
        ('openinterest',None),
        ('adj_close',5),
        ('dema_short', 7),
        ('dema_long', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )

class TestDEMA(bt.Strategy):
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

def DEMA(data, time_period, column):
    # Calcualte DEMA
    EMA = data[column].ewm(span=time_period, adjust=False).mean()
    DEMA = 2*EMA - EMA.ewm(span=time_period, adjust=False).mean()

    return DEMA

def DEMA_strategy(data):
    buy_list = []
    sell_list = []
    flag = False
    # Loop through the data
    for i in range(0, len(data)):
        if data['DEMA_short'][i] > data['DEMA_long'][i] and flag == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag = True
        elif data['DEMA_short'][i] < data['DEMA_long'][i] and flag == True:
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            flag = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    # store buy and sell signal/lists into the data set
    data['Buy'] = buy_list
    data['Sell'] = sell_list

def run_DEMA(df):
    df['DEMA_short'] = DEMA(df, 20, 'Close')
    df['DEMA_long'] = DEMA(df, 50, 'Close')
    # Run the stretegy to get the buy and sell signals
    DEMA_strategy(df)