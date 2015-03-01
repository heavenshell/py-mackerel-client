# -*- coding: utf-8 -*-
"""
    mackerel.host
    ~~~~~~~~~~~~~

    Mackerel client implemented by Pyton.

    Ported from `mackerel-client-ruby`.
    <https://github.com/mackerelio/mackerel-client-ruby>

    :copyright: (c) 2014 Hatena, All rights reserved.
    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import re


class Host(object):
    MACKEREL_INTERFACE_NAME_PATTERN = re.compile(r'^eth\d')

    def __init__(self, **kwargs):
        self.args = kwargs
        self.name = kwargs.get('name')
        self.meta = kwargs.get('meta')
        self.type = kwargs.get('type')
        self.status = kwargs.get('status')
        self.memo = kwargs.get('memo')
        self.is_retired = kwargs.get('isRetired')
        self.id = kwargs.get('id')
        self.created_at = kwargs.get('createdAt')
        self.roles = kwargs.get('roles')
        self.interfaces = kwargs.get('interfaces')

    def ip_addr(self):
        pass

    def mac_addr(self):
        pass

