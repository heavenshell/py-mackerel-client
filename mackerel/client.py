# -*- coding: utf-8 -*-
"""
    mackerel.client
    ~~~~~~~~~~~~~~~

    Mackerel client implemented by Pyton.

    Ported from `mackerel-client-ruby`.
    <https://github.com/mackerelio/mackerel-client-ruby>

    :copyright: (c) 2014 Hatena, All rights reserved.
    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import requests
import simplejson as json
import mackerel.host import Host

class MackerelClientError(Exception):
    pass


class Client(object):
    ERROR_MESSAGE_FOR_API_KEY_ABSENCE = 'API key is absent. Set your API key in a environment variable called MACKEREL_APIKEY.'

    def __init__(self, **kwargs):
        self.origin = kwargs.get('mackerel_origin', 'https://mackerel.io')
        api_key = kwargs('mackerel_api_key', None)
        if api_key is None:
            raise MackerelClientError(self.ERROR_MESSAGE_FOR_API_KEY_ABSENCE)

    def get_host(self, host_id):
        uri = '{0}/api/v0/hosts/{1}'.format(self.origin, host_id)
        data = self._request(uri)

        return Host(data['host'])

    def update_host_status(self, host_id, status):
        pass

    def retire_host(self, host_id):
        pass

    def post_metrics(self, metrics):
        pass

    def get_latest_metrics(self, host_ids, names):
        pass

    def post_service_metrics(self, service_name, metrics):
        pass

    def get_hosts(self, opts=None):
        pass

    def _request(self, uri, headers=None, params=None):
        if headers is not None:
            headers.update({'X-Api-Key': self.api_key})

        res = requests.get(uri, headers=headers, params=params)

        if res.status_code != '200':
            message = 'GET {0} failed: {1}'.format(uri, res.status_code)
            raise MackerelClientError(message)

        data = json.dumps(res.content)

        return data
