from mootdx.quotes import Quotes
import pandas as pd
# code = '512010'
client = Quotes.factory(market='std')



# df = pd.read_csv('etf/all_etf.csv',header=None)
# for code in df[0]:
#     df = pd.DataFrame()
#     idx = 0
#     while True:
#         data = client.bars(symbol=f'{code}',frequency=0,start=idx,offset=800)
#         idx += len(data)

#         df = pd.concat([df,data.iloc[::-1]])
#         print(len(data))
#         if len(data) <= 0:
#             break
#     df.iloc[::-1].to_csv(f'etf/{code}.min.csv')
from mootdx.consts import MARKET_SH,MARKET_SZ
code = '159915'
df = pd.DataFrame()
idx = 0
while True:
    data = client.bars(symbol=f'{code}',frequency=0,start=idx,offset=800)
    # data = client.index(frequency=0, market=MARKET_SZ, symbol='399006', start=idx, offset=800)
    idx += len(data)

    df = pd.concat([df,data.iloc[::-1]])
    print(len(data))
    if len(data) <= 0:
        break
df.iloc[::-1].to_csv(f'{code}.min.csv')
