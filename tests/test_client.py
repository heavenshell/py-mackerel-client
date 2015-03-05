# -*- coding: utf-8 -*-
"""
    mackerel.tests.test_client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mackerel client tests.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import requests
from unittest import TestCase
from mock import patch
from mackerel.client import Client, MackerelClientError
from mackerel.host import Host


def dummy_response(m, filename):
    response = requests.Response()
    response.status_code = 200
    root_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_path, filename)
    with open(file_path, 'r') as f:
        data = f.read()
        response._content = data
        m.return_value = response


class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.environ.get('MACKEREL_API_KEY')
        cls.client = Client(mackerel_api_key=api_key)

    def test_should_get_hosts(self):
        """ Client().get_hosts() should get host list. """
        hosts = self.client.get_hosts()
        for host in hosts:
            self.assertTrue(isinstance(host, Host))

    @patch('mackerel.client.requests.get')
    def test_should_get_host(self, m):
        """ Client().get_hosts() should get host. """
        dummy_response(m, 'fixtures/get_host.json')
        host = self.client.get_host('2k64NJ5Ncrs')
        self.assertTrue(isinstance(host, Host))

    #@patch('mackerel.client.requests.post')
    def test_should_update_host_poweroff(self):#, m):
        """ Client().update_host_status('poweroff') should return success. """
        #dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status('2k48zsCx8ij', 'poweroff')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k64NJ5Ncrs')
        self.assertEqual(host.status, 'poweroff')

    def test_should_update_host_standby(self):
        """ Client().update_host_status('standby') should return success. """
        ret = self.client.update_host_status('2k48zsCx8ij', 'standby')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k64NJ5Ncrs')
        self.assertEqual(host.status, 'standby')

    def test_should_update_host_working(self):
        """ Client().update_host_status('working') should return success. """
        ret = self.client.update_host_status('2k48zsCx8ij', 'working')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k64NJ5Ncrs')
        self.assertEqual(host.status, 'working')

    def test_should_update_host_maintenance(self):
        """ Client().update_host_status('maintenance') should return success. """
        ret = self.client.update_host_status('2k64NJ5Ncrs', 'maintenance')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k64NJ5Ncrs')
        self.assertEqual(host.status, 'maintenance')

    def test_should_update_host_invalid(self):
        """ Client().update_host_status('foo') should raise error. """
        with self.assertRaises(MackerelClientError):
            self.client.update_host_status('2k64NJ5Ncrs', 'foo')

    def test_should_retire(self):
        """ Client().retire_host() should return success. """
        #ret = self.client.retire_host('2k48zsCx8ij')
        #self.assertEqual(ret['success'], True)

    def test_should_get_latest_metrics(self):
        """ Client().get_latest_metrics() should get metrics. """
        ret = self.client.get_latest_metrics(['2k64NJ5Ncrs'],
                                             ['loadavg5', 'memory.free'])
        for k in ['loadavg5', 'memory.free']:
            self.assertTrue(k in ret['tsdbLatest']['2k64NJ5Ncrs'].keys())

    def test_should_post_metrics(self):
        """ Client().post_metrics() should return success. """
        id = '2k64NJ5Ncrs'
        metrics = [
            {
                'hostId': id, 'name': 'custom.metrics.loadavg',
                'time': 1401537844, 'value': 1.4
            },
            {
                'hostId': id, 'name': 'custom.metrics.uptime',
                'time': 1401537844, 'value': 500
            }

        ]
        ret = self.client.post_metrics(metrics)
        self.assertEqual(ret['success'], True)

    def test_should_post_service_metrics(self):
        """ Client().post_service_metrics() should return success. """
        metrics = [
            {
                'name': 'custom.metrics.latency',
                'time': 1401537844, 'value': 0.5
            },
            {
                'name': 'custom.metrics.uptime',
                'time': 1401537844, 'value': 500
            }
        ]
        ret = self.client.post_service_metrics('service_name', metrics)
        self.assertEqual(ret['success'], True)

    def test_should_raise_error_when_service_not_found(self):
        """ Client().post_service_metrics() should raise error when service name not found. """
        metrics = [
            {
                'name': 'custom.metrics.latency',
                'time': 1401537844, 'value': 0.5
            },
            {
                'name': 'custom.metrics.uptime',
                'time': 1401537844, 'value': 500
            }
        ]
        with self.assertRaises(MackerelClientError):
            self.client.post_service_metrics('foobarbaz', metrics)
