import backtrader as bt # 导入 Backtrader
import backtrader.indicators as btind # 导入策略分析模块

import pandahouse as ph
import datetime
import numpy as np
import pandas as pd
import math
conn = {
    'database':'stock_data',
    'host':'http://127.0.0.1:8123',
    'user':'default',
    'password' : '',
}

class ACommission(bt.CommInfoBase):

    params = (
        ('stamp_duty',0.001),
        ('percabs',True)
    )

    def _getcommission(self, size, price, pseudoexec):
        
        if size > 0:
            return size * price * self.p.commission
        elif size < 0:
            return - size * price * (self.p.stamp_duty + self.p.commission)
        else:
            return 0


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        
        self.dataclose = self.datas[0].close
        self.sma = btind.SMA(self.dataclose, period=5)

        self.sign_buy = self.dataclose > 1.01 * self.sma
        self.sing_sell = self.dataclose < self.sma
        # print(self.sma)

        # self.params = (
        #     ('sma1_period', 20),
        #     ('sma2_period', 50)
        # )

        # self.sma1 = bt.indicators.SimpleMovingAverage(
        #     self.dataclose, period=10)
        # self.sma2 = bt.indicators.SimpleMovingAverage(
        #     self.dataclose, period=50)
        # self.crossover = bt.indicators.CrossOver(self.sma1, self.sma2)


    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])
        current_date = self.datas[0].datetime.date(0)
        print("Current backtest date:", current_date)
        print(self.data.open[0],self.data.close[0])
        # if not self.position:
        #     if self.crossover > 0:
        #         self.buy(size=100)
        # elif self.crossover < 0:
        #     self.sell(size=100)
        cash = self.broker.get_cash()

        #  # 如果上一时间点价格高出五天平均价1%, 则全仓买入
        if self.sign_buy[0] and cash > 0:

            size = int(cash / self.data.close[0] / 100) * 100  # 计算最大可用资金买入的股数
            if size >= 100:
                print(f"create order size : {size}")
                self.order = self.buy(size=max(size, 100))
        elif self.sing_sell and self.getposition(self.data).size > 0:
            # 记录这次卖出
            # 卖出所有股票,使这只股票的最终持有量为0
            pos = self.getposition()
            self.sell(size=pos.size)
            # self.sell()
            # self.order_target_percent(target=0)
        # print(self.broker.get_cash())
        # print(MA5)
        # if self.dataclose[0] < self.dataclose[-1]:
        #     # current close less than previous close

        #     if self.dataclose[-1] < self.dataclose[-2]:
        #         # previous close less than the previous close

        #         # BUY, BUY, BUY!!! (with all possible default parameters)
        #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #         self.buy(size=100)
        # if self.dataclose[0] > self.dataclose[-1]:
        #     # current close less than previous close

        #     if self.dataclose[-1] > self.dataclose[-2]:
        #         # previous close less than the previous close

        #         # BUY, BUY, BUY!!! (with all possible default parameters)
        #         self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #         self.sell(size=100)


    def notify_order(self, order):
    # 未被处理的订单
        if order.status in [order.Submitted, order.Accepted]:
            return
        # 已经处理的订单
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            if order.isbuy():
                self.log(
                        'BUY EXECUTED, ref:%.0f,Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
                        (order.ref, # 订单编号
                        order.executed.price, # 成交价
                        order.executed.value, # 成交额
                        order.executed.comm, # 佣金
                        order.executed.size, # 成交量
                        order.data._name)) # 股票名称
            else: # Sell
                self.log('SELL EXECUTED, ref:%.0f, Price: %.2f, Cost: %.2f, Comm %.2f, Size: %.2f, Stock: %s' %
                            (order.ref,
                            order.executed.price,
                            order.executed.value,
                            order.executed.comm,
                            order.executed.size,
                            order.data._name))


# Add a strategy
start_time = '2020-02-01'
end_time = '2020-12-31'
sql = f'select trade_date as date,open,close,high,low,volume,adjfactor from stock_data.stock_daily where stock_code == 1 and trade_date >= \'{start_time}\' and trade_date <= \'{end_time}\' order by date ASC'
print(sql)
df = ph.read_clickhouse(sql,connection=conn)
df.drop(df[df['close'] == -1].index,inplace=True)
df.index = pd.to_datetime(df['date'])

new_df = pd.DataFrame()
new_df['close'] = round(df['adjfactor'] * (df.iloc[0]['close'] / df.iloc[0]['adjfactor']) / 100,2)
new_df['open'] = round(df['open'] / df['close'] * new_df['close'],2)
new_df['high'] = round(df['high'] / df['close'] * new_df['close'],2)
new_df['low'] = round(df['low'] / df['close'] * new_df['close'],2)
new_df['volume'] = df['volume']

df['close'] = round(df['close'] / 100,2)
df['open'] = round(df['open'] / 100,2)
df['high'] = round(df['high'] / 100,2)
df['low'] = round(df['low'] / 100,2)

print(df)
start_cash = 10000.0

# 实例化 cerebro
cerebro = bt.Cerebro()

datafeed = bt.feeds.PandasData(dataname=new_df, fromdate=datetime.datetime(2020,2,24), todate=datetime.datetime(2020,12,31))

cerebro.adddata(datafeed, name='000001') # 通过 name 实现数据集与股票的一一对应


cerebro.broker.setcash(start_cash)
comm = ACommission(stamp_duty=0.001,commission=0.0001)
cerebro.broker.addcommissioninfo(comm)
# cerebro.broker.set_slippage_fixed(fixed=0.02,slip_open=True,
#                    slip_match=False,
#                    slip_out=True)
cerebro.broker.set_slippage_fixed(fixed=0.02,slip_open=True,
                   slip_match=True,
                   slip_out=True)
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='pnl') # 返回收益率时序数据
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='_AnnualReturn') # 年化收益率
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='_SharpeRatio') # 夏普比率
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='_DrawDown') # 回撤

cerebro.addstrategy(TestStrategy)


print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
# # # 启动回测
res = cerebro.run()
# daily_return = pd.Series(res[0].analyzers.pnl.get_analysis())
print("--------------- AnnualReturn -----------------")
print(res[0].analyzers._AnnualReturn.get_analysis())
print("--------------- SharpeRatio -----------------")
print(res[0].analyzers._SharpeRatio.get_analysis())
print("--------------- DrawDown -----------------")
print(res[0].analyzers._DrawDown.get_analysis())
# # # 打印回测完成后的资金
print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
pnl = port_value - start_cash  # 盈亏统计

print(f"总资金: {round(port_value, 2)}")
print(f"净收益: {round(pnl, 2)}")


cerebro.plot(style='candlestick')  # 画图