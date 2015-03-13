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


def dummy_response(m, filename, status_code=200):
    response = requests.Response()
    response.status_code = status_code
    root_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(root_path, filename)
    with open(file_path, 'r') as f:
        data = f.read()
        response._content = data
        m.return_value = response


class TestClient(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.environ.get('MACKEREL_APIKEY')
        cls.client = Client(mackerel_api_key=api_key)
        cls.id = 'xxxxxxxxxxx'

    @patch('mackerel.client.requests.get')
    def test_should_get_hosts(self, m):
        """ Client().get_hosts() should get host list. """
        dummy_response(m, 'fixtures/get_hosts.json')
        hosts = self.client.get_hosts()
        for host in hosts:
            self.assertTrue(isinstance(host, Host))

    @patch('mackerel.client.requests.get')
    def test_should_get_host(self, m):
        """ Client().get_hosts() should get host. """
        dummy_response(m, 'fixtures/get_host.json')
        host = self.client.get_host(self.id)
        self.assertTrue(isinstance(host, Host))

    @patch('mackerel.client.requests.post')
    def test_should_update_host_poweroff(self, m):
        """ Client().update_host_status('poweroff') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status(self.id, 'poweroff')
        self.assertEqual(ret['success'], True)
        with patch('mackerel.client.requests.get') as m:
            dummy_response(m, 'fixtures/poweroff.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'poweroff')

    @patch('mackerel.client.requests.post')
    def test_should_update_host_standby(self, m):
        """ Client().update_host_status('standby') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status(self.id, 'standby')
        self.assertEqual(ret['success'], True)

        with patch('mackerel.client.requests.get') as m:
            dummy_response(m, 'fixtures/standby.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'standby')

    @patch('mackerel.client.requests.post')
    def test_should_update_host_working(self, m):
        """ Client().update_host_status('working') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status('2k48zsCx8ij', 'working')
        self.assertEqual(ret['success'], True)
        with patch('mackerel.client.requests.get') as m:
            dummy_response(m, 'fixtures/working.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'working')

    @patch('mackerel.client.requests.post')
    def test_should_update_host_maintenance(self, m):
        """ Client().update_host_status('maintenance') should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.update_host_status(self.id, 'maintenance')
        self.assertEqual(ret['success'], True)
        with patch('mackerel.client.requests.get') as m:
            dummy_response(m, 'fixtures/maintenance.json')
            host = self.client.get_host(self.id)
            self.assertEqual(host.status, 'maintenance')

    def test_should_update_host_invalid(self):
        """ Client().update_host_status('foo') should raise error. """
        with self.assertRaises(MackerelClientError):
            self.client.update_host_status(self.id, 'foo')

    @patch('mackerel.client.requests.post')
    def test_should_retire(self, m):
        """ Client().retire_host() should return success. """
        dummy_response(m, 'fixtures/success.json')
        ret = self.client.retire_host(self.id)
        self.assertEqual(ret['success'], True)

    @patch('mackerel.client.requests.get')
    def test_should_get_latest_metrics(self, m):
        """ Client().get_latest_metrics() should get metrics. """
        dummy_response(m, 'fixtures/get_latest_metrics.json')
        ret = self.client.get_latest_metrics([self.id],
                                             ['loadavg5', 'memory.free'])
        for k in ['loadavg5', 'memory.free']:
            self.assertTrue(k in ret['tsdbLatest'][self.id].keys())

    @patch('mackerel.client.requests.post')
    def test_should_post_metrics(self, m):
        """ Client().post_metrics() should return success. """
        dummy_response(m, 'fixtures/success.json')
        id = self.id
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

    @patch('mackerel.client.requests.post')
    def test_should_post_service_metrics(self, m):
        """ Client().post_service_metrics() should return success. """
        dummy_response(m, 'fixtures/success.json')
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

    @patch('mackerel.client.requests.post')
    def test_should_raise_error_when_service_not_found(self, m):
        """ Client().post_service_metrics() should raise error when service name not found. """
        dummy_response(m, 'fixtures/error.json', 404)
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


class TestHost(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key = os.environ.get('MACKEREL_APIKEY')
        cls.client = Client(mackerel_api_key=api_key)
        cls.id = 'xxxxxxxxxxx'

    @patch('mackerel.client.requests.get')
    def test_should_get_ipaddress(self, m):
        """ Host().ipa_ddr() should get ipaddress. """
        dummy_response(m, 'fixtures/get_host.json')
        host = self.client.get_host(self.id)
        self.assertEqual(host.ip_addr(), '10.0.2.15')
