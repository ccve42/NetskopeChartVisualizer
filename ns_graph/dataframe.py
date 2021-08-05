import os
import collections.abc
import datetime
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ns_graph.utils import (
    norm_ts,
    autopct,
    output_path,
)
from ns_graph._log import logging


today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)

DATE = last_month.strftime("%Y%m")


class Dataframe:

    def __init__(self, data):
        self.df = pd.json_normalize(data)
        self.DF = norm_ts(self.df)

    def clean(self):
        self.DF = clean_df(self.DF)

    def int32(self):
        """ Change int64, float64 to int32, float32. """
        self.DF = self.DF.astype({col: 'int32' for col in
                                  self.DF.select_dtypes('int64').columns})
        self.DF = self.DF.astype({col: 'float32' for col in
                                  self.DF.select_dtypes('float64').columns})

    def drop_duplicates(self):
        self.DF = self.DF.drop_duplicates(subset=['timestamp','user'])

    def unknown2others(self):
        self.DF.loc[self.DF['ccl'] == "unknown", "ccl"] = "Others"

    def merge_ios(self):
        self.DF.loc[self.DF['device'] == "iPhone", "device"] = "iOS Device"

    def merge_macos(self):
        self.DF.loc[self.DF['os'] == "Sierra", "os"] = "Mac OS"
        self.DF.loc[self.DF['os'] == "El Capitan", "os"] = "Mac OS"
        self.DF.loc[self.DF['os'] == "Catalina", "os"] = "Mac OS"

    def drop_apple(self):
        self.DF = self.DF[~self.DF["site"].str.contains('apple', na=False)]
        self.DF = self.DF[~self.DF["site"].str.contains('microsoft', na=False)]
        self.DF = self.DF[~self.DF["site"].str.contains('Adjust', na=False)]


class Graph(Dataframe):

    def __init__(self, dic):
        super().__init__(dic)
        # Japanese compatibility
        matplotlib.rc('font', family='TakaoPGothic')

    def piechart(self, kind):
        """ os, device, browser """

        count = self.DF[kind].value_counts()
        plt.figure()
        matplotlib.style.use('seaborn-pastel')
        count.plot(kind='pie',
                   subplots=False,
                   figsize=(10, 7),
                   autopct=autopct,
                   startangle=90,
                   counterclock=False,
                   legend=True,
                   labels=None,)

        plt.legend(labels=count.index,
                   loc='upper left',
                   bbox_to_anchor=(1, 1),
                   fancybox=True,)
        plt.xlabel('')
        plt.ylabel('')
        plt.tight_layout() # take bbox(legend) into account
        plt.savefig(output_path(f"{DATE}_3.2-4.{kind}.png"))
        plt.close()

    def ccl_napp(self):

        df = pd.DataFrame()
        df['app'] = self.DF['app'].tolist()
        df['ccl'] = self.DF['ccl'].tolist()
        count = df.groupby('ccl')['app'].value_counts()
        count = count.rename('napp').reset_index()
        count = count['ccl'].value_counts()

        plt.figure()
        matplotlib.style.use('seaborn-pastel')
        count.plot(kind='pie',
                   subplots=False,
                   figsize=(10, 7),
                   autopct=autopct,
                   startangle=90,
                   counterclock=False,
                   legend=True,
                   labels=None,)

        plt.legend(labels=count.index,
                   loc='upper left',
                   bbox_to_anchor=(1, 1),
                   fancybox=True,)
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.6.1_pie.png"))
        plt.close()

        plt.figure()
        matplotlib.style.use('seaborn')
        count.plot(kind='barh',
                   subplots=False,
                   figsize=(8, 5),
                   legend=False,
                   color=['C0', 'C1', 'C2', 'C3', 'C4'],)
        plt.gca().invert_yaxis() # Plot in ascending order
        plt.xticks(rotation=0)
        plt.ylabel('Applications')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.6.1_bar.png"))
        plt.close()


    def ccl_nuser(self):

        df = pd.DataFrame()
        df['user'] = self.DF['user'].tolist()
        df['ccl'] = self.DF['ccl'].tolist()
        count = df.groupby('ccl')['user'].value_counts()
        count = count.rename('napp').reset_index()
        count = count['ccl'].value_counts()

        plt.figure()
        matplotlib.style.use('seaborn-pastel')
        count.plot(kind='pie',
                   subplots=False,
                   figsize=(10, 7),
                   autopct=autopct,
                   startangle=90,
                   counterclock=False,
                   legend=True,
                   labels=None,)

        plt.legend(labels=count.index,
                   loc='upper left',
                   bbox_to_anchor=(1, 1),
                   fancybox=True,)
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.6.2_pie.png"))
        plt.close()

        plt.figure()
        matplotlib.style.use('seaborn')
        count.plot(kind='barh',
                   subplots=False,
                   figsize=(8, 5),
                   color=['C0', 'C1', 'C2', 'C3', 'C4'],
                   legend=False,)
        plt.gca().invert_yaxis() # Plot in ascending order
        plt.xticks(rotation=0)
        plt.ylabel('Active Users')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.6.2_bar.png"))
        plt.close()


    def pie_category(self):
        """ category """

        df = pd.DataFrame()
        df['category'] = self.DF['category'].tolist()
        df['app'] = self.DF['app'].tolist()
        df.drop_duplicates(subset=['category','app'])
        df.loc[df['category'] == "Uncategorized", "category"] = "Others"
        count = df['category'].value_counts().reset_index()
        logging.debug(count)
        count.loc[count.index >= 5, "index"] = "Others"
        logging.debug(count)
        count = count.groupby('index')['category'].value_counts()
        count = count.rename('ncategory').reset_index()
        count.drop(columns='ncategory', inplace=True)
        others = count.loc[count['index'] == "Others"]
        count.drop(others.index, inplace=True)
        count = count.sort_values(by='category', ascending=False)
        others = others['category'].sum()
        logging.debug(others)
        others = pd.DataFrame(data={'index':'Others','category':others,},
                              index=[0],)
        df = pd.concat([count, others], ignore_index=True)
        df = df.set_index('index')
        logging.debug(df)

        plt.figure()
        matplotlib.style.use('seaborn-pastel')
        df.plot(kind='pie',
                subplots=True,
                figsize=(10, 7),
                autopct=autopct,
                startangle=90,
                counterclock=False,
                legend=True,
                labels=None,)

        plt.legend(labels=df.index,
                   loc='upper left',
                   bbox_to_anchor=(1, 1),
                   fancybox=True,)
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.7_category_pie.png"))
        plt.close()


    def pie_dayweek(self):

        df = pd.DataFrame()
        df['timestamp'] = self.DF['timestamp'].dt.day_name()
        df['user'] = self.DF['user'].tolist()
        df = df.drop_duplicates(subset=['timestamp','user'])
        count = df['timestamp'].value_counts()
        plt.figure()
        matplotlib.style.use('seaborn-pastel')

        count.plot(kind='pie',
                   subplots=False,
                   figsize=(10, 7),
                   autopct=autopct,
                   startangle=90,
                   counterclock=False,
                   legend=True,
                   labels=None,)

        plt.legend(labels=count.index,
                   loc='upper left',
                   bbox_to_anchor=(1, 1),
                   fancybox=True,)
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.1_day_of_week.png"))
        logging.debug(count.index)
        plt.close()


    def user_hourly(self):

        df = pd.DataFrame()
        df['timestamp'] = self.DF['timestamp'].dt.hour.tolist()
        df['user'] = self.DF['user'].tolist()
        df = df.drop_duplicates(subset=['timestamp','user'])
        df = df.groupby(['timestamp','user']).size().count(level='timestamp')

        plt.figure()
        matplotlib.style.use('seaborn')
        df.plot(kind='bar',
                subplots=False,
                figsize=(8, 5),
                legend=False,)
        plt.xticks(rotation=0)
        plt.xlabel('Time / Hour')
        plt.ylabel('Active Users')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.1_hourly.png"))
        plt.close()


    def user_timeline(self):

        df = pd.DataFrame()
        df['timestamp'] = self.DF['timestamp'].dt.hour.tolist()
        df['user'] = self.DF['user'].tolist()
        df.drop_duplicates(subset=['timestamp','user'])
        df.loc[df['timestamp'].isin(range(6)), "timestamp"] = "0-5"
        df.loc[df['timestamp'].isin(range(6,10)), "timestamp"] = "6-9"
        df.loc[df['timestamp'].isin(range(10,18)), "timestamp"] = "10-17"
        df.loc[df['timestamp'].isin(range(18,22)), "timestamp"] = "18-21"
        df.loc[df['timestamp'].isin(range(22,25)), "timestamp"] = "22-24"
        df = df.groupby(['timestamp','user']).size().count(level='timestamp')

        plt.figure()
        matplotlib.style.use('seaborn-pastel')
        df.plot(kind='pie',
                subplots=False,
                figsize=(10, 7),
                autopct=autopct,
                startangle=90,
                counterclock=False,
                legend=False,)

        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.1_timeline.png"))
        plt.close()


    def bar_app_daily(self, name):
    ### App incidents / day
        df = pd.DataFrame()
        df['timestamp'] = self.DF['timestamp'].tolist()
        df.index = df['timestamp']
        df = df['timestamp'].value_counts().resample('D').count()

    ### Change axis name to clean date name.
    # Reset index to modify name because index is immutable.
        df = df.rename_axis('timestamp2').reset_index()
    # Simplify dates.
        df['timestamp2'] = df['timestamp2'].dt.date
    # Put it back to index after renaming.
        df.index = df['timestamp2']

        plt.figure()
        matplotlib.style.use('seaborn')
        df.plot(kind='bar',
                subplots=False,
                figsize=(13, 9),
                legend=False,)

        plt.xticks(fontsize=8, rotation=70)
        plt.xlabel('')
        plt.ylabel('Total Events')
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_{name}.png"))
        plt.close()


    def hist_top5cat(self):
        """ make top 5 category graphs """

        # Get a list of the top 5 categories.
        df = pd.DataFrame()
        df['category'] = self.DF['category'].tolist()
        df.loc[df['category'] == "Uncategorized", "category"] = "Others"
        count = df['category'].value_counts().reset_index()
        count.loc[count.index >= 6, "index"] = "Others"
        count = count.groupby('index')['category'].value_counts()
        count = count.rename('ncategory').reset_index()
        count.drop(columns='ncategory',
                   inplace=True,)
        others = count.loc[count['index'] == "Others"]
        count.drop(others.index,
                   inplace=True,)
        count = count.sort_values(by='category',
                                  ascending=False,)
        others = others['category'].sum()
        others = pd.DataFrame(data={'index':'Others','category':others,},
                              index=[0],)
        df = pd.concat([count, others],
                       ignore_index=True,)
        df = df.set_index('index').head(5)
        top5cat = df.index.tolist()

        count = 0
        # Plot Collaboration Stack Bar Chart and Save as png file.
        for cat in top5cat:
            count += 1
            pivot_df = stack_bar_pd(self.DF, category=cat)

            plt.figure()
            matplotlib.style.use('seaborn')
            pivot_df.plot.bar(stacked=True,
                              figsize=(13,9),)
            plot_settings('Time / hour')
            plt.xticks(fontsize=8, rotation=70)
            plt.legend(title='',
                       loc='upper center',
                       ncol=5,
                       fontsize='small',)
            plt.tight_layout()
            plt.savefig(output_path(f"{DATE}_3.7.{str(count)}.png"))
            plt.close()


    def npa_top5(self):
        pivot_df = stack_bar_for_npa(self.DF)

        plt.figure()
        matplotlib.style.use('seaborn')
        pivot_df.plot.bar(stacked=True,
                          figsize=(13,9),)
        plot_settings('Time / hour')
        plt.xticks(fontsize=8, rotation=70)
        plt.legend(title='',
                   loc='upper center',
                   ncol=5,
                   fontsize='small',)
        plt.tight_layout()
        plt.savefig(output_path(f"{DATE}_3.8.png"))
        plt.close()


class tools:
    @staticmethod
    def list2fset(x):
        if isinstance(x, collections.Hashable):
            pass
        #print(x)
        else:
            x = tuple(x)
            #print(x)
        return x

    @staticmethod
    def to_hash_obj(df):
        df = df.apply(lambda x: tools.list2fset(x))
        #print(df.head())
        return(df)

    @staticmethod
    def norm_ts(df):
        """ Timestamp conversion in df column.

            First convert epoch to readable dates.
            Then UTC to Asia/Tokyo.
        """
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df.timestamp = df.timestamp.dt.tz_localize('UTC').dt.tz_convert('Asia/Tokyo')
        return df

    @staticmethod
    def gby_appc_site(df):
        df = df.groupby(['timestamp','appcategory','site']).count()
        return df

    @staticmethod
    def describe(df):
        df = df.groupby(['timestamp','appcategory','site']).describe()
        return df


def unique_user(df):
    df = tools.to_hash_obj(df)
    uuser = df.user.nunique()
    return uuser

def clean_df(df):
    df = tools.to_hash_obj(df)
    #df = tools.norm_ts(df)
    df.dropna(axis=1, inplace=True)
    return df

def count_values(df, column):
    """ Count column values, sort and return top 5 items with count. """
    df2 = df.groupby(column)['timestamp'].count().sort_values(ascending=False).head(5)
    return df2


def stack_bar_pd(df, category):
    df2 = pd.DataFrame()
    df2 = df[['timestamp','site','user']][df['category'] == category]

    df2['timestamp'] = df2['timestamp'].dt.date
    df2 = df2.groupby(['timestamp','site']).count()
    logging.debug(df2)
    df2 = df2.reset_index()
    logging.debug(df2)

    pivot_df = df2.pivot(index='timestamp',
                         columns='site',
                         values='user').fillna(0)
    top5 = pivot_df.sum(axis=0,
                        skipna=True).sort_values(ascending=False).head()
    top5 = top5.index.tolist()
    pivot_df = pivot_df[top5]
    return pivot_df


def stack_bar_for_npa(df):
    df2 = pd.DataFrame()
    df2 = df[['timestamp','site','user']]

    df2['timestamp'] = df2['timestamp'].dt.date
    df2 = df2.groupby(['timestamp','site']).count()
    logging.debug(df2)
    df2 = df2.reset_index()
    logging.debug(df2)

    pivot_df = df2.pivot(index='timestamp',
                         columns='site',
                         values='user').fillna(0)
    top5 = pivot_df.sum(axis=0,
                        skipna=True).sort_values(ascending=False).head()
    top5 = top5.index.tolist()
    pivot_df = pivot_df[top5]
    return pivot_df


def plot_settings(xlabel):
    plt.xlabel("")
    plt.ylabel("Total Events")
    plt.xticks(rotation=45)


class Table(Dataframe):
    """ Make tables and save as excel file. """
    def get_tops_by_value(self, key: str, value: str, number_tops: int):
        """
        dataframe:
        site    number_user
        """
        df = self.DF.groupby(key)[value].count().sort_values(ascending=False).head(number_tops).to_frame('number_events')
        df = df.reset_index()
        return df

    def get_number_of_unique_users_in_category(self, site_name):
        df = self.DF[self.DF["site"] == site_name]
        return df.user.nunique()

    def get_number_of_events_in_category(self, site_name):
        df = self.DF[self.DF["site"] == site_name]
        return len(df)

    def cleaner(self, dataframe, category):
        """ remove .0 in the category column """
        dataframe[category] = dataframe[category].astype(str)
        dataframe[category] = dataframe[category].str.replace('.0', ' ', regex=True)
        #dataframe[category] = dataframe[category].astype(int)
        return dataframe

    def make_table_npa(self):
        """
        dataframe:
        site    number_user    number_events

        make df and sort by events number at the end.
        """
        df = self.get_tops_by_value("site", "user", 50)
        number_row = len(df.index)
        assert len(df) <= 50
        for i in range(number_row):
            site_name = df.at[i, 'site']
            df.loc[df.index == i, "unique_users"] = self.get_number_of_unique_users_in_category(site_name)
        return self.cleaner(df, 'unique_users')

    def df2excel(self, df, sheetname):
        """ Save df as xlsx file. """
        name = "".join((sheetname, ".xlsx"))
        df.to_excel(name, index=False)
