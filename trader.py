import backtrader
import pandas as pd
from strategies.strategy import TestStrategy
from strategies.SMA import TestSMA,PandasSMA,run_SMA
from strategies.OBV import TestOBV,PandasOBV,run_OBV
from strategies.DEMA import TestDEMA,PandasDEMA,run_DEMA


def get_data(symbol,start, end):

    # Load the data
    if symbol.upper() == 'AMZN':
        df = pd.read_csv('data/AMZN.csv')
    elif symbol.upper() == 'TSLA':
        df = pd.read_csv("data/TSLA.csv")
    elif symbol.upper() == 'GOOG':
        df = pd.read_csv("data/GOOG.csv")
    elif symbol.upper() == 'AAPL':
        df = pd.read_csv("data/AAPL.csv")
    else:
        df = pd.read_csv("data/oracle.csv")

    # Get the data range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    # Set the start and end index rown to 0
    start_row = 0
    end_row = 0

    # Match the user selection (date) to the date in dataset (search start date)
    for i in range(0, len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break
    # Match the user selection (date) to the date in dataset (search end date)
    for j in range(0, len(df)):
        if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row = len(df)-1-j
            break
    # Set the index to be the date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row + 1, :]


cerebro = backtrader.Cerebro()

cerebro.addsizer(backtrader.sizers.FixedSize, stake=1000)

cerebro.broker.set_cash(1000000)

strategy_name = input("What strategy do you want to choose?")

df = get_data('AAPL','2020, 1, 22','2021, 1, 22')

if strategy_name == 'SMA':
    run_SMA(df)
    data = PandasSMA(dataname=df)
    cerebro.addstrategy(TestSMA)
elif strategy_name == 'OBV':
    run_OBV(df)
    data = PandasOBV(dataname=df)
    cerebro.addstrategy(TestOBV)
elif strategy_name == 'DEMA':
    run_DEMA(df)
    data = PandasDEMA(dataname=df)
    cerebro.addstrategy(TestDEMA)
else:
    data = backtrader.feeds.PandasData(dataname=df)
    cerebro.addstrategy(TestStrategy)

cerebro.adddata(data)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
