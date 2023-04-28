import collections
import datetime

import backtrader as bt  # 升级到最新版
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import akshare as ak  # 升级到最新版
import pandas as pd
import backtrader.indicators as btind # 导入策略分析模块

# stock_hfq_df = pd.read_csv('t.csv')
stock_hfq_df = pd.read_csv('etf/hfq/510210.csv',index_col='datetime',parse_dates=['datetime'])
# stock_hfq_df.to_csv('t.csv',index=False)

# stock_hfq_df = stock_hfq_df.resample('15min').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum', 'amount': 'sum'}).dropna()
print(stock_hfq_df)


# class TestStrategy(bt.Strategy):

#     def log(self, txt, dt=None):
#         ''' Logging function fot this strategy'''
#         dt = dt or self.datas[0].datetime.date(0)
#         print('%s, %s' % (dt.isoformat(), txt))
        
#     def __init__(self):
#         # Keep a reference to the "close" line in the data[0] dataseries

#         self.buy_counter = 0  # 初始化交易计数器
#         self.sell_counter = 0  # 初始化交易计数器
#         self.last_bar_date = None  # 初始化上一个交易日的日期

#         MA1 = 30
#         MA2 = 60
#         self.dataclose = self.datas[0].close
#         self.sma1 = btind.SMA(self.dataclose, period=MA1)
#         self.sma2 = btind.SMA(self.dataclose, period=MA2)

#         self.sign_buy = self.sma1 > self.sma2
#         self.sing_sell = self.sma1 < self.sma2


#         # print(self.sma)

#         # self.params = (
#         #     ('sma1_period', 20),
#         #     ('sma2_period', 50)
#         # )

#         # self.sma1 = bt.indicators.SimpleMovingAverage(
#         #     self.dataclose, period=10)
#         # self.sma2 = bt.indicators.SimpleMovingAverage(
#         #     self.dataclose, period=50)
#         # self.crossover = bt.indicators.CrossOver(self.sma1, self.sma2)


#     def next(self):
#         # Simply log the closing price of the series from the reference
#         # self.log('Close, %.2f' % self.dataclose[0])

#         if self.last_bar_date is None or self.last_bar_date != self.data.datetime.date(0):
#             self.buy_counter = 0
#             self.sell_counter = 0
#         self.last_bar_date = self.data.datetime.date(0)

#         current_date = self.datas[0].datetime.date(0)
        
#         print("Current backtest date:", )
#         # print(self.data.open[0],self.data.close[0])
#         # if not self.position:
#         #     if self.crossover > 0:
#         #         self.buy(size=100)
#         # elif self.crossover < 0:
#         #     self.sell(size=100)
#         cash = self.broker.get_cash()
#         if self.sign_buy[0] and cash > 0 and self.buy_counter < 1:

#             size = int(cash / self.data.close[0] / 100) * 100  # 计算最大可用资金买入的股数
#             if size >= 100:
#                 print(f"create order size : {size}")
#                 self.order = self.buy(size=max(size, 100))
#                 self.buy_counter += 1
#         elif self.sing_sell and self.getposition(self.data).size > 0 and self.sell_counter < 1:
#             # 记录这次卖出
#             # 卖出所有股票,使这只股票的最终持有量为0
#             pos = self.getposition()
#             self.sell(size=pos.size)
#             self.sell_counter += 1

#     def notify_order(self, order):
#     # 未被处理的订单
#         if order.status in [order.Submitted, order.Accepted]:
#             return
#         # 已经处理的订单
#         if order.status in [order.Completed, order.Canceled, order.Margin]:
#             if order.isbuy():
#                 self.log(
#                         'BUY EXECUTED, ref:%.0f,Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
#                         (order.ref, # 订单编号
#                         order.executed.price, # 成交价
#                         order.executed.value, # 成交额
#                         order.executed.comm, # 佣金
#                         order.executed.size, # 成交量
#                         order.data._name)) # 股票名称
#             else: # Sell
#                 self.log('SELL EXECUTED, ref:%.0f, Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
#                             (order.ref,
#                             order.executed.price,
#                             order.executed.value,
#                             order.executed.comm,
#                             order.executed.size,
#                             order.data._name))

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s %s, %s' % (dt.isoformat(),self.datas[0].datetime.time(0),txt))
        
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries

        self.dataclose = self.datas[1].close
        self.dataopen = self.datas[0].open
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

    def next(self):

        if self.data.datetime.time() == datetime.time(9, 35): # 检查是否是第一个5分钟线
            # print(self.dataclose[0] ,self.dataclose[-1])
            if self.dataclose[0] < self.dataclose[-1]:
                cash = self.broker.get_cash()
                size = int(cash / self.data.close[0] / 100) * 100  # 计算最大可用资金买入的股数
                if size >= 100:
                    # print(f"create order size : {size}")
                    self.order = self.buy(size=max(size, 100))

        elif self.data.datetime.time() == datetime.time(14, 55): # 检查是否是收盘时间
            pos = self.getposition()
            self.sell(size=pos.size)

        # cash = self.broker.get_cash()
        # if self.sign_buy[0] and cash > 0:

        #     size = int(cash / self.data.close[0] / 100) * 100  # 计算最大可用资金买入的股数
        #     if size >= 100:
        #         print(f"create order size : {size}")
        #         self.order = self.buy(size=max(size, 100))
        #         self.buy_counter += 1
        # elif self.sing_sell and self.getposition(self.data).size > 0:
        #     # 记录这次卖出
        #     # 卖出所有股票,使这只股票的最终持有量为0
        #     pos = self.getposition()
        #     self.sell(size=pos.size)
        #     self.sell_counter += 1

    # def notify_order(self, order):
    # # 未被处理的订单
    #     if order.status in [order.Submitted, order.Accepted]:
    #         return
    #     # 已经处理的订单
    #     if order.status in [order.Completed, order.Canceled, order.Margin]:
    #         if order.isbuy():
    #             self.log(
    #                     'BUY EXECUTED, ref:%.0f,Price: %.4f, Cost: %.4f, Comm %.4f, Size: %.4f, Stock: %s' %
    #                     (order.ref, # 订单编号
    #                     order.executed.price, # 成交价
    #                     order.executed.value, # 成交额
    #                     order.executed.comm, # 佣金
    #                     order.executed.size, # 成交量
    #                     order.data._name)) # 股票名称
    #         else: # Sell
    #             self.log('SELL EXECUTED, ref:%.0f, Price: %.4f, Cost: %.4f, Comm %.4f, Size: %.4f, Stock: %s' %
    #                         (order.ref,
    #                         order.executed.price,
    #                         order.executed.value,
    #                         order.executed.comm,
    #                         order.executed.size,
    #                         order.data._name))

cerebro = bt.Cerebro()  # 初始化回测系统
start_date = datetime.datetime(2023, 1, 1)  # 回测开始时间

end_date = datetime.datetime(2023,4, 1)  # 回测结束时间
data = bt.feeds.PandasData(dataname=stock_hfq_df, fromdate=start_date, todate=end_date)  # 加载数据


sh_csv = pd.read_csv('etf/hfq/000001.csv',index_col='datetime',parse_dates=['datetime'])
# sh_csv = pd.read_csv('etf/hfq/510050.csv',index_col='datetime',parse_dates=['datetime'])
sh = bt.feeds.PandasData(dataname=sh_csv, fromdate=start_date, todate=end_date)  # 加载数据

cerebro.adddata(data)  # 将数据传入回测系统
cerebro.adddata(sh)
cerebro.addstrategy(TestStrategy)  # 将交易策略加载到回测系统中
# strats = cerebro.optstrategy(TestStrategy,maperiod=range(10, 31))
start_cash = 10000
cerebro.broker.setcash(start_cash)  # 设置初始资本为 100000
# cerebro.addsizer(bt.sizers.FixedSize, stake=10)
cerebro.broker.setcommission(commission=0.00006)  # 设置交易手续费为 0.2%


# 返回年初至年末的年度收益率
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn')
# 计算最大回撤相关指标
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown')
# 计算年化收益：日度收益
cerebro.addanalyzer(bt.analyzers.Returns, _name='_Returns', tann=252)
# 计算年化夏普比率：日度收益
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio', timeframe=bt.TimeFrame.Days, annualize=True, riskfreerate=0) # 计算夏普比率
cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='_SharpeRatio_A')
# 返回收益率时序
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='_TimeReturn')



result = cerebro.run()  # 运行回测系统

port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
pnl = port_value - start_cash  # 盈亏统计

print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")

print("--------------- AnnualReturn -----------------")
print(result[0].analyzers._AnnualReturn.get_analysis())
print("--------------- DrawDown -----------------")
print(result[0].analyzers._DrawDown.get_analysis())
print("--------------- Returns -----------------")
print(result[0].analyzers._Returns.get_analysis())
print("--------------- SharpeRatio -----------------")
print(result[0].analyzers._SharpeRatio.get_analysis())
print("--------------- SharpeRatio_A -----------------")
print(result[0].analyzers._SharpeRatio_A.get_analysis())

cerebro.plot(style='candlestick')  # 画图
