import akshare as ak


stock_hfq_df = ak.stock_zh_a_hist(symbol="000001", adjust="hfq",start_date='20200104',end_date='20230301').iloc[:, :6]

print(stock_hfq_df)