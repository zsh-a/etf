import pandas as pd
s = 'datetime,open,high,low,close,volume,amount\n'
filename = '000001.SH.csv'
with open(f"hfq/{filename}", "r") as f:
    for line in f:
        # 使用逗号分割每一行数据
        data = line.strip().split(",")
        # 将时间点的字符串进行切片，分离小时和分钟
        hour = data[1][:2]
        minute = data[1][2:]
        # 将小时和分钟拼接为一个时间点，并添加":"分隔符
        time_point = data[0] + " " + hour + ":" + minute
        # 输出合并后的结果
        s += time_point + "," + ",".join(data[2:]) + '\n'

with open(f"hfq/{filename.split('.')[0]}.csv", "w") as f:
    f.write(s)
