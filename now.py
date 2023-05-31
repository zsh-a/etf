# from mootdx.quotes import Quotes

# client = Quotes.factory(market='std')

# client.quotes(symbol=["000001", "510050"]).to_csv('now.csv')
# # print(client.quotes(symbol=["000001", "510050"]))

# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# df = pd.read_csv(
#     "etf/hfq/510210.csv", index_col="datetime", parse_dates=["datetime"]
# )
# df['rtn'] = np.log(df['close']) - np.log(df['close'].shift(1))
# print(df['rtn'])
# df=df.dropna()

# # df['rtn'].plot()
# plt.plot(df['rtn'])
from mootdx.quotes import Quotes
import pandas as pd
from mootdx.consts import * 

# code = '512010'
client = Quotes.factory(market='std')
data = client.index(frequency=0, market=MARKET_SZ, symbol='399006', start=0, offset=800)
# data = client.bars(symbol=f'399006',frequency=0,offset=800)
print(data)