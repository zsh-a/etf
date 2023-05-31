import struct
from pathlib import Path
from collections import OrderedDict
import pandas as pd
import os

def _parse_date(num):
    """
    解析日期
    :param num:
    :return:
    """
    month = (num % 2048) // 100
    year = num // 2048 + 2004
    day = (num % 2048) % 100

    return year, month, day

def _parse_time(num):
    """
    解析时间
    :param num:
    :return:
    """
    return (num // 60), (num % 60)


def unpack_records(fmt, data):
    """
    解包
    :param fmt:
    :param data:
    :return:
    """
    record = struct.Struct(fmt)
    t = record.unpack_from(data, 0)
    print(t,_parse_date(t[0]),_parse_time(t[1]))
    result = (record.unpack_from(data, offset) for offset in range(0, len(data), record.size))

    return result


def parse_data_by_file(filename):
        """

        :param filename:
        :return:
        """
        print(filename)
        content = Path(filename).read_bytes()
        raw_li = unpack_records("<HHfffffII", content)  # noqa

        data = []

        for row in raw_li:
            year, month, day = _parse_date(row[0])
            hour, minute = _parse_time(row[1])

            data.append(
                OrderedDict(
                    [
                        ("date", f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"),
                        ("year", year),
                        ("month", month),
                        ("day", day),
                        ("hour", hour),
                        ("minute", minute),
                        ("open", row[2]),
                        ("high", row[3]),
                        ("low", row[4]),
                        ("close", row[5]),
                        ("amount", row[6]),
                        ("volume", row[7]),
                        # ('unknown', row[8])
                    ]
                )
            )

        return data

def get_df(code_or_file, **kwargs):
    """
    :param code_or_file:
    :param kwargs:
    :return:
    """
    df = pd.DataFrame(data=parse_data_by_file(code_or_file))
    df.index = pd.to_datetime(df.date)
    df = df[["open", "high", "low", "close", "amount", "volume"]]

    return df

base_dir = 'min1'
def gen(filename):
    fmt = "<HHfffffII"
    df = pd.read_csv(f'min1/data/{filename}',index_col='datetime')
    code = filename.split('.')[0]
    mkt = 'sh' if code[0] == '5' else 'sz'
    f = open(f'min1/tdx/{mkt}{code}.lc5','wb')
    buf = bytearray(struct.calcsize(fmt) * len(df))

    idx = 0
    for index,row in df.iterrows():
        op = row['open']
        close = row['close']
        high = row['high']
        low = row['low']
        amount = row['amount']
        volume = row['vol']
        year = row['year']
        month = row['month']
        day = row['day']
        hour = row['hour']
        minute = row['minute']
        # print(index.year,index.month,index.day,index.hour,index.minute)
        record = struct.Struct(fmt)
        # record.pack(index.year,index.month,index.day,index.hour,index.minute)
        # bs = record.pack((indexyear - 2004)  * 2048 + index.month * 100 + index.day,index.hour * 60 + index.minute,open,high,low,close,amount,int(volume),0)
        record.pack_into(buf,idx,(year - 2004)  * 2048 + month * 100 + day,hour * 60 + minute,op,high,low,close,amount,int(volume),0)
        idx += record.size


    f.write(buf)


# for file in os.listdir('min'):
#     gen(f'{file}')

gen('999999.min.csv')

