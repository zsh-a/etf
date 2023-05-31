from mootdx.quotes import Quotes
import pandas as pd
# code = '512010'
client = Quotes.factory(market='std')



from mootdx.consts import MARKET_SH,MARKET_SZ
code = '510880'
df = pd.DataFrame()
idx = 0
while True:
    # data = client.bars(symbol=f'{code}',frequency=8,start=idx,offset=800)
    data = client.index(frequency=8, market=MARKET_SH, symbol='999999', start=idx, offset=800)
    idx += len(data)

    df = pd.concat([df,data.iloc[::-1]])
    print(len(data))
    if len(data) <= 0:
        break
df.iloc[::-1].to_csv(f'etf/min1/data/999999.min.csv')
# df.iloc[::-1].to_csv(f'etf/min1/data/{code}.min.csv')
