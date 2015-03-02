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
from mackerel.client import Client
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
        host = self.client.get_host('xxxxxxxxxxx')
        self.assertTrue(isinstance(host, Host))
