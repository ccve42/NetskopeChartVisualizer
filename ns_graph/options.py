import argparse

from ns_graph.version import __version__


def parseArgs(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-v', '--version', action='version',
        version=__version__,
        help='print program version and exit')
    parser.add_argument(
        '-m', '--month',
        type=int,
        default=1,
        help='select a number of months of data necessary')
    parser.add_argument(
        'tenant',
        type=str,
        help='specify a tenant name')
    parser.add_argument(
        'token',
        type=str,
        help='enter a token of the tenant.')
    parser.add_argument(
        '--type',
        default='application',
        choices=['application', 'page', 'network', 'anomaly',
                 'Compromised Credential', 'policy', 'Legal Hold',
                 'malsite', 'Malware', 'DLP',
                 'Security Assessment', 'watchlist', 'quarantine',
                 'Remediation', 'uba'],
        type=str,
        help='specify a data type to download')
    parser.add_argument(
        '--endpoint',
        default='events',
        choices=['alerts', 'events'],
        type=str,
        help='specify the endpoint')
    parser.add_argument(
        '--query',
        default=None,
        type=str,
        help='enter a query')
    parser.add_argument(
        '--save-as-json',
        action='store_true', dest='save_as_json', default=False,
        help='save downloaded data as JSON file')
    parser.add_argument(
        '--save-as-csv',
        action='store_true', dest='save_as_csv', default=False,
        help='save downloaded data as CSV file')
    parser.add_argument(
        '--load-csv', metavar='<CSV file>',
        default=None,
        help='load a CSV file')
    parser.add_argument(
        '--load-json', metavar='<JSON file>',
        default=None,
        help='load a JSON file')
    parser.add_argument(
        '--save-only',
        action='store_true', dest='save_only', default=False,
        help='save downloaded data as CSV file')
    parser.add_argument(
        '--logs',
        action='store_true', dest='logs', default=False,
        help='output the log file')
    parser.add_argument(
        '--private-apps',
        action='store_true', dest='private_apps', default=False,
        help='make graphs of private apps')
    parser.add_argument(
        '--dlp',
        action='store_true', dest='dlp', default=False,
        help='make graphs of DLP')

    parser.add_argument_group('general')

    parser = parser.parse_args(*args)
    return parser
