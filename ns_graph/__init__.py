#!/usr/bin/env python

import re
import sys
import json

from ns_graph._log import logging
from ns_graph.options import (
    parseArgs,
)
from ns_graph.api import (
    API
)
from ns_graph.dataframe import (
    Graph,
    Table,
)
from ns_graph._config import (
    pd_set,
)
from ns_graph.utils import (
    check_dir,
)
from ns_graph.message import (
    success,
)


if sys.version_info < (3, 6, 0):
    raise ImportError('ns-graph requires Python version >= 3.6.  Installed is %s' % (sys.version_info,))

def options():
    parser = parseArgs(sys.argv[1:])
    opts = {
        'month': parser.month,
        'tenant': parser.tenant,
        'token': parser.token,
        'endpoint': parser.endpoint,
        'query': parser.query,
        'type' : parser.type,
        'logs': parser.logs,
        'save_as_json': parser.save_as_json,
        'save_as_csv': parser.save_as_csv,
        'load_json': parser.load_json,
        'load_csv': parser.load_csv,
        'save_only': parser.save_only,
        'private_apps': parser.private_apps,
        'dlp': parser.dlp,
    }
    return opts


def make_graph_events(graph):
    graph.drop_duplicates()
    # perf optimization
    graph.int32()
    # do plot labels pretty
    graph.merge_ios()
    graph.merge_macos()
    graph.drop_apple()
    # 3.1
    graph.pie_dayweek()
    graph.user_hourly()
    graph.user_timeline()
    # 3.2 - 3.4
    graph.piechart('os')
    graph.piechart('browser')
    graph.piechart('device')
    # 3.6.1
    graph.ccl_napp()
    # 3.6.2
    graph.ccl_nuser()
    # 3.7
    graph.pie_category()
    # 3.7.1 - 3.7.5
    graph.hist_top5cat()
    # 3.8
    graph.bar_app_daily('3.8_RTP')


def make_graph_private_apps(graph, table):
    # 3.8
    graph.npa_top5()
    table.df2excel(table.make_table_npa(), sheetname='npa')


def make_graph_dlp(graph):
    # 3.10
    graph.bar_app_daily('3.10_dlp')


def main():
    opts = options()
    if opts.get('load_json') is not None:
        logging.info('loading JSON')
        with open(f"{opts.get('load_json')}", 'r') as f:
            data = json.load(f)

    else:
        test = API(opts.get('tenant'),
                   opts.get('token'),
                   opts.get('endpoint'),
                   opts.get('query'),
                   opts.get('type'),
                   opts.get('month'))
        test.main()

        if opts.get('save_as_json'):
            logging.info('dumping downloaded data as JSON')
            with open(f"{opts.get('tenant')}.json", 'w') as f:
                json.dump(test.data, f)
        if opts.get('save_as_csv'):
            logging.info('dumping downloaded data as csv')
            import pandas as pd
            df = pd.json_normalize(test.data)
            df.to_csv(f"{opts.get('tenant')}.csv", index=None)

    if not opts.get('save_only'):
        data = test.data

        check_dir('png')
        logging.info('it may take some time to convert the data to dataframe...')
        graph = Graph(data)
        table = Table(data)

        if opts.get('private_apps'):
            check_dir('xlsx')
            make_graph_private_apps(graph, table)
        elif opts.get('dlp'):
            make_graph_dlp(graph)
        else:
            make_graph_events(graph)
    success()


__all__ = ['main']
