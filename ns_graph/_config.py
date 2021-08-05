import pandas as pd

def pd_settings():
    """  Pandas df Display Settings """
    pd.set_option('expand_frame_repr', True)
    pd.set_option('max_columns', 999)
    pd.set_option('max_rows', 999)
    pd.set_option('max_colwidth', 40)

def pd_set():
    """  Pandas df Display Settings """
    pd.set_option('display.max_columns', 999)
    pd.set_option('display.max_rows', 999)
    pd.set_option('display.width', 40)
