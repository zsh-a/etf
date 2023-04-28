import torch
import torch.nn as nn

import torch.nn.functional as F

import backtrader as bt # 导入 Backtrader
import pandahouse as ph
import datetime
import numpy as np
import pandas as pd
from pylab import mpl,plt
conn = {
    'database':'stock_data',
    'host':'http://127.0.0.1:8123',
    'user':'default',
    'password' : '',
}



class Module(nn.Module):
    def __init__(self) -> None:
        super(self,Module).__init__()

        self.fc1 = nn.Linear(128,256)
        self.fc2 = nn.Linear(256,128)

        self.fc = nn.Linear(128,5)
    def forward(self,x):
        x = F.gelu(self.fc1(x))
        x = F.gelu(self.fc2(x))
        out = self.fc(x)
        return out



# sql = 'select close from stock_data.stock_daily where stock_code == 1 and trade_date > \'2023-02-01\''
# df = ph.read_clickhouse(sql,connection=conn)

# model = Module()
sql = 'select trade_date as datetime,open,high,low,close,volume from stock_data.stock_daily where stock_code == 1 and trade_date > \'2020-02-01\''
print(sql)
df =ph.read_clickhouse(sql,connection=conn)
print(df)
short = df['close'].rolling(42).mean()
long = df['close'].rolling(252).mean()


# plt.style.use('seaborn')
mpl.rcParams['savefig.dpi'] = 300
mpl.rcParams['font.family'] = 'serif'
data = pd.DataFrame()
data['close'] = df['close']
data['short'] = short
data['long'] = long


data.plot(title='EUR/USD | 42 & 252 days SMAs', figsize=(10, 6))
# print(df['close'].rolling(42).mean())
