import backtrader as bt
import math
import numpy as np

class PandasOBV(bt.feeds.PandasData):
    lines = ('obv','obv_ema','buy_signal','sell_signal')
    params = (
        ('datetime', None),
        ('open',1),
        ('high',2),
        ('low',3),
        ('close',4),
        ('volume',6),
        ('openinterest',None),
        ('adj_close',5),
        ('obv', 7),
        ('obv_ema', 8),
        ('buy_signal', 9),
        ('sell_signal',10)
    )

class TestOBV(bt.Strategy):
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


def buy_sell(signal, col1, col2):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

# Loop through the length of the data set
    for i in range(0, len(signal)):
        # If OBV > OBV_EMA Then Buy--> col1 =>'OBV' and col2 => 'OBV_EMA'
        if signal[col1][i] > signal[col2][i] and flag != 1:
            sigPriceBuy.append(signal['Close'][i])
            sigPriceSell.append(np.nan)
            flag = 1
        # If OBV < OBV_EMA Then Sell
        elif signal[col1][i] < signal[col2][i] and flag != 0:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(signal['Close'][i])
            flag = 0
        else:
            sigPriceSell.append(np.nan)
            sigPriceBuy.append(np.nan)

    return(sigPriceBuy, sigPriceSell)


def run_OBV(df):

    # Calcualte the on Blaance Volume (OBV)
    OBV = []
    OBV.append(0)

    # Loop throught the data set (close proce) from the second row (index 1) to the end of the data set
    for i in range(1, len(df.Close)):
        if df.Close[i] > df.Close[i-1]:
            OBV.append(OBV[-1]+df.Volume[i])
        elif df.Close[i] < df.Close[i-1]:
            OBV.append(OBV[-1]-df.Volume[i])
        else:
            OBV.append(OBV[-1])

    # Store the OBV and OBV Exponential Moving Average (EMA) into new column
    df['OBV'] = OBV
    df['OBV_EMA'] = df['OBV'].ewm(span=20).mean()

    # Create buy and sell columns
    x = buy_sell(df, 'OBV', 'OBV_EMA')
    df['Buy_Signal_Price'] = x[0]
    df['Sell_Signal_Price'] = x[1]


