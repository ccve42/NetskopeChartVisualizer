import os
import collections.abc
import pandas as pd
import datetime as dt
import pytz

from dateutil.relativedelta import *

def df2excel(df, abspath, sheetname):
    """ Save df in xlsx file. """
    import openpyxl
    with pd.ExcelWriter(abspath, engine="openpyxl", mode="a") as writer:
        df.to_excel(writer, sheet_name=sheetname)

def check_dir(dir_name):
    dir_path = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

def output_path(fname, which='png'):
    """ Return abspath to imgdir concatonated w/ the parameter, fname
    """
    output_path = os.path.join(os.getcwd(), which)
    full_path = os.path.join(output_path, fname)
    return full_path

def dic2df(dic):
    df = pd.json_normalize(dic['data'])
    return df

def list2fset(x):
    if isinstance(x, collections.Hashable):
        pass
    #print(x)
    else:
        x = tuple(x)
        #print(x)
    return x

def to_hash_obj(df):
    df = df.apply(lambda x: list2fset(x))
    #print(df.head())
    return(df)

def norm_ts(df):
    """ Timestamp conversion in df column.

        First convert epoch to readable dates.
        Then UTC to Asia/Tokyo.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.timestamp = df.timestamp.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
    return df

def autopct(pct):
    return ('%1.1f%%' % pct) if pct > 3.3 else ''

def get_new_labels(sizes, labels):
    new_labels = [label if size > 3.3 else '' for size, label in zip(sizes, labels)]
    return new_labels

def show_memory(df, df2):
    """ Compare memory of two dfs. """
    log.logging.debug("test df: ",
                      str(df.memory_usage(index=True, deep=True).sum()))
    log.logging.debug("test2 df: ",
                      str(df2.memory_usage(index=True, deep=True).sum()))

def get_origindates(nMonth: int):
    """ return timestamp """
    nMonth -= 1
    now = dt.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
    end = now.replace(day=1, hour=23, minute=59, second=59, microsecond=999999) - dt.timedelta(days=1)
    start = end.replace(hour=0, minute=0, second=0, microsecond=0, day=1) - relativedelta(months=nMonth)
    return int(start.timestamp()), int(end.timestamp())
