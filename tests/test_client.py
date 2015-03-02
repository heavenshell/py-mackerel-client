# -*- coding: utf-8 -*-
"""
    mackerel.tests.test_client
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mackerel client tests.


    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
from unittest import TestCase
from mackerel.client import Client, MackerelClientError
from mackerel.host import Host


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

    def test_should_get_host(self):
        """ Client().get_hosts() should get host. """
        host = self.client.get_host('2k48zsCx8ij')
        self.assertTrue(isinstance(host, Host))

    def test_should_update_host_poweroff(self):
        """ Client().update_host_status('poweroff') should return success. """
        ret = self.client.update_host_status('2k48zsCx8ij', 'poweroff')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k48zsCx8ij')
        self.assertEqual(host.status, 'poweroff')

    def test_should_update_host_standby(self):
        """ Client().update_host_status('standby') should return success. """
        ret = self.client.update_host_status('2k48zsCx8ij', 'standby')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k48zsCx8ij')
        self.assertEqual(host.status, 'standby')

    def test_should_update_host_working(self):
        """ Client().update_host_status('working') should return success. """
        ret = self.client.update_host_status('2k48zsCx8ij', 'working')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k48zsCx8ij')
        self.assertEqual(host.status, 'working')

    def test_should_update_host_maintenance(self):
        """ Client().update_host_status('maintenance') should return success. """
        ret = self.client.update_host_status('2k48zsCx8ij', 'maintenance')
        self.assertEqual(ret['success'], True)
        host = self.client.get_host('2k48zsCx8ij')
        self.assertEqual(host.status, 'maintenance')

    def test_should_update_host_invalid(self):
        """ Client().update_host_status('foo') should raise error. """
        with self.assertRaises(MackerelClientError):
            self.client.update_host_status('2k48zsCx8ij', 'foo')

    def test_should_retire(self):
        """ Client().retire_host() should return success. """
        ret = self.client.retire_host('2k48zsCx8ij')
        self.assertEqual(ret['success'], True)
