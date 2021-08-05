from certifi import where
from pytz import timezone
from requests import get
from urllib3 import PoolManager
from urllib.parse import quote
import datetime as dt

from ns_graph._log import logging
from ns_graph.utils import get_origindates


class URL:
    """ Paginated Netskope REST API URL creater/updater.
    """
    def __init__(self, tenant: str, token: str, endpoint: str,
                 query: str, kind: str, month: int):
        self.tenant = tenant
        self.token = token
        self.endpoint = endpoint
        self.query =  None if query is None else quote(query)
        self.type = kind
        self.month = month
        self.get_last_month_epoch()
        self.update_url()

    def pagination(self, last_timestamp):
        self.update_endtime(last_timestamp)
        self.update_url()

    def update_url(self):
        if self.query is not None:
            self.apiurl = f"https://{self.tenant}.goskope.com/api/v1/{self.endpoint}?token={self.token}&query={self.query}&type={self.type}&starttime={self.starttime}&endtime={self.endtime}"
        else:
            self.apiurl = f"https://{self.tenant}.goskope.com/api/v1/{self.endpoint}?token={self.token}&type={self.type}&starttime={self.starttime}&endtime={self.endtime}"

    def get_last_month_epoch(self):
        """ Get Unix time of the first and last date of the last month.
        -> Last Month / 01 / 00:00:00:000000 - self.starttime
        -> Last Month / 31 / 23:59:59:999999 - self.endtime
        """
        self.starttime, self.endtime = get_origindates(self.month)

    def update_endtime(self, last_timestamp):
        """ Grab a timestamp of the last object and subtract it by 1.
        """
        self.endtime = last_timestamp - 1
        logging.info('New Endtime: %s', dt.datetime.fromtimestamp(self.endtime, tz=timezone('Asia/Tokyo')))


class API(URL):
    def __init__(self, tenant: str, token: str, endpoint: str,
                 query: str, kind: str, month: int):
        super().__init__(tenant, token, endpoint, query, kind, month)
        self.data = []

    def get_cert(self):
        ssl = PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=where())
        ssl.request('GET', f'https://{self.tenant}.goskope.com')

    def _get_data(self, apiurl):
        response = get(self.apiurl)
        return response.json()

    def _append_object(self, raw_data) -> list:
        for index in range(0, len(raw_data['data'])):
            self.data.append(raw_data['data'][index])

    def is_5000(self, raw_data):
        return len(raw_data) == 5000

    def main(self):
        """ Get log data via REST API.
        If the parsed log objects are 5000 in total, repeat the function
        until the parsed log is less than 5000.
        """
        logging.info('getting SSL certification of the site')
        self.get_cert()
        logging.info(f'endpoint: {self.apiurl}')
        raw_data = self._get_data(self.apiurl)
        assert raw_data['status'] == 'success', "data['status'] returned error."
        self._append_object(raw_data)
        logging.info('Objects: %d', len(self.data))

        while self.is_5000(raw_data['data']):
            last_timestamp = self.data[-1]['timestamp']
            self.pagination(last_timestamp)
            logging.info('End: %s', self.endtime)
            logging.info('Start: %s', self.starttime)
            raw_data = self._get_data(self.apiurl)
            if raw_data['status'] != 'success':
                while raw_data['status'] != 'success':
                    raw_data = self._get_data(self.apiurl)
            self._append_object(raw_data)
            logging.info('Objects: %d', len(self.data))
