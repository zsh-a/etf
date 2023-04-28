import collections
from datetime import datetime

import backtrader as bt  # 升级到最新版
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import akshare as ak  # 升级到最新版
import pandas as pd

# plt.rcParams["font.sans-serif"] = ["SimHei"]
# plt.rcParams["axes.unicode_minus"] = False

# 利用 AKShare 获取股票的后复权数据，这里只获取前 6 列
# stock_hfq_df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq",start_date='20200104',end_date='20230301').iloc[:, :6]
# 处理字段命名，以符合 Backtrader 的要求
# stock_hfq_df.columns = [
#     'date',
#     'open',
#     'close',
#     'high',
#     'low',
#     'volume',
# ]
# 把 date 作为日期索引，以符合 Backtrader 的要求

stock_hfq_df = pd.read_csv('t.csv')
stock_hfq_df.index = pd.to_datetime(stock_hfq_df['date'])
# stock_hfq_df.to_csv('t.csv',index=False)
print(stock_hfq_df)

# class MyStrategy(bt.Strategy):
#     """
#     主策略程序
#     """
#     params = (("maperiod", 20),)  # 全局设定交易策略的参数

#     def __init__(self):
#         """
#         初始化函数
#         """
#         self.data_close = self.datas[0].close  # 指定价格序列
#         # 初始化交易指令、买卖价格和手续费
#         self.order = None
#         self.buy_price = None
#         self.buy_comm = None
#         # 添加移动均线指标
#         self.sma = bt.indicators.SimpleMovingAverage(
#             self.datas[0], period=self.params.maperiod
#         )

#     def next(self):
#         """
#         执行逻辑
#         """
#         if self.order:  # 检查是否有指令等待执行,
#             return
#         # 检查是否持仓
#         if not self.position:  # 没有持仓
#             if self.data_close[0] > self.sma[0]:  # 执行买入条件判断：收盘价格上涨突破20日均线
#                 self.order = self.buy(size=100)  # 执行买入
#         else:
#             if self.data_close[0] < self.sma[0]:  # 执行卖出条件判断：收盘价格跌破20日均线
#                 self.order = self.sell(size=100)  # 执行卖出


# Create a Stratey
# class TestStrategy(bt.Strategy):
#     params = (
#         ('maperiod', 15),
#     )

#     def log(self, txt, dt=None):
#         ''' Logging function fot this strategy'''
#         dt = dt or self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))

#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries
#         self.dataclose = self.datas[0].close

#         # To keep track of pending orders and buy price/commission
#         self.order = None
#         self.buyprice = None
#         self.buycomm = None

#         # Add a MovingAverageSimple indicator
#         self.sma = bt.indicators.SimpleMovingAverage(
#             self.datas[0], period=self.params.maperiod)
        
#         bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
#         bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
#                                             subplot=True)
#         bt.indicators.StochasticSlow(self.datas[0])
#         bt.indicators.MACDHisto(self.datas[0])
#         rsi = bt.indicators.RSI(self.datas[0])
#         bt.indicators.SmoothedMovingAverage(rsi, period=10)
#         bt.indicators.ATR(self.datas[0], plot=False)

#     def notify_order(self, order):
#         if order.status in [order.Submitted, order.Accepted]:
#             # Buy/Sell order submitted/accepted to/by broker - Nothing to do
#             return

#         # Check if an order has been completed
#         # Attention: broker could reject order if not enough cash
#         if order.status in [order.Completed]:
#             if order.isbuy():
#                 self.log(
#                     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                     (order.executed.price,
#                      order.executed.value,
#                      order.executed.comm))

#                 self.buyprice = order.executed.price
#                 self.buycomm = order.executed.comm
#             else:  # Sell
#                 self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
#                          (order.executed.price,
#                           order.executed.value,
#                           order.executed.comm))

#             self.bar_executed = len(self)

#         elif order.status in [order.Canceled, order.Margin, order.Rejected]:
#             self.log('Order Canceled/Margin/Rejected')

#         self.order = None

#     def notify_trade(self, trade):
#         if not trade.isclosed:
#             return

#         self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
#                  (trade.pnl, trade.pnlcomm))

#     def next(self):
#         # Simply log the closing price of the series from the reference
#         self.log('Close, %.2f' % self.dataclose[0])

#         # Check if an order is pending ... if yes, we cannot send a 2nd one
#         if self.order:
#             return

#         # Check if we are in the market
#         if not self.position:

#             # Not yet ... we MIGHT BUY if ...
#             if self.dataclose[0] > self.sma[0]:

#                 # BUY, BUY, BUY!!! (with all possible default parameters)
#                 self.log('BUY CREATE, %.2f' % self.dataclose[0])

#                 # Keep track of the created order to avoid a 2nd order
#                 self.order = self.buy()

#         else:

#             if self.dataclose[0] < self.sma[0]:
#                 # SELL, SELL, SELL!!! (with all possible default parameters)
#                 self.log('SELL CREATE, %.2f' % self.dataclose[0])

#                 # Keep track of the created order to avoid a 2nd order
#                 self.order = self.sell()

class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 5),
        ('printlog', False),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        print(self.dataclose[0])
        current_date = self.datas[0].datetime.date(0)
        print("Current backtest date:", current_date)
        cash = self.broker.get_cash()
        print(cash)
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.order_target_value(target=cash)

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.order_target_value(target=0)

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), doprint=True)

cerebro = bt.Cerebro()  # 初始化回测系统
start_date = datetime(2020, 1, 6)  # 回测开始时间
end_date = datetime(2020,3, 1)  # 回测结束时间
data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据
cerebro.adddata(data)  # 将数据传入回测系统
cerebro.addstrategy(TestStrategy)  # 将交易策略加载到回测系统中
# strats = cerebro.optstrategy(TestStrategy,maperiod=range(10, 31))
start_cash = 1000000
cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
# cerebro.addsizer(bt.sizers.FixedSize, stake=10)
cerebro.broker.setcommission(commission=0.001)  # 设置交易手续费为 0.2%
cerebro.run()  # 运行回测系统

port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
pnl = port_value - start_cash  # 盈亏统计

print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")

cerebro.plot(style='candlestick')  # 画图
