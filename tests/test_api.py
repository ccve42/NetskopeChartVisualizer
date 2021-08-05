import unittest
import requests

from ns_graph import api


class TestUrl(unittest.TestCase):
    def setUp(self):
        self.url = api.url("application", tenant_name="TED")

    def test_url(self):
        response = requests.get(self.url.apiurl)
        self.assertEqual(200, response.status_code)
        content = response.json()
        self.assertEqual('success', content['status'])

    def test_pagination(self):
        self.url.pagination(8888)
        self.assertEqual(8887, self.url.month.end)
        self.assertNotEqual(8886, self.url.month.end)


class TestEpoch(unittest.TestCase):
    def setUp(self):
        self.epoch = api.epoch()

    def test_timezone(self):
        self.assertEqual('Asia/Tokyo', self.epoch._TODAY.tzinfo.zone)

    def test_time(self):
        end_hour = self.epoch._END.strftime('%H')
        end_minute = self.epoch._END.strftime('%M')
        end_second = self.epoch._END.strftime('%S')
        end_mSecond = self.epoch._END.strftime('%f')
        end_day = int(self.epoch._END.strftime('%d'))

        self.assertEqual('23', end_hour)
        self.assertEqual('59', end_minute)
        self.assertEqual('59', end_second)
        self.assertEqual('999999', end_mSecond)
        # End day must be equal or greater than 28th.
        self.assertGreaterEqual(end_day, 28)

        start_hour = self.epoch._START.strftime('%H')
        start_minute = self.epoch._START.strftime('%M')
        start_second = self.epoch._START.strftime('%S')
        start_mSecond = self.epoch._START.strftime('%f')
        start_day = self.epoch._START.strftime('%d')

        self.assertEqual('00', start_hour)
        self.assertEqual('00', start_minute)
        self.assertEqual('00', start_second)
        self.assertEqual('000000', start_mSecond)
        self.assertEqual('01', start_day)

        self.assertIsInstance(self.epoch.START, int)
        self.assertIsInstance(self.epoch.end, int)


class TestGetData(unittest.TestCase):
    def setUp(self):
        self.url = api.url("application", tenant_name="TED")
        self.data = api._get_data(self.url.apiurl)
        self.assertEqual('success', self.data['status'])

    def test_data(self):
        self.assertIsInstance(self.data['data'], list)
        self.assertEqual(5000, len(self.data['data']))

class TestUtil(unittest.TestCase):
    def setUp(self):
        self.url = api.url("application", tenant_name="TED")
        self.data = api._get_data(self.url.apiurl)
        self.assertEqual('success', self.data['status'])

    def test_append_object(self):
        self.empty_storage = []
        self.assertEqual(5000, len(self.data['data']))
        self.storage = api.util.append_object(self.data, self.empty_storage)
        self.assertEqual(5000, len(self.storage))
