import backtrader
import datetime
from strategy import TestStrategy

cerebro = backtrader.Cerebro()

cerebro.addsizer(backtrader.sizers.FixedSize, stake=1000)

cerebro.broker.set_cash(1000000)
data = backtrader.feeds.YahooFinanceCSVData(
    dataname='oracle.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2001, 10, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2001, 12, 1),
    reverse=False)

cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)
cerebro.run()

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
