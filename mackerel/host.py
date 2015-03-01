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
        self.name = kwargs.get('name', None)
        self.meta = kwargs.get('meta', None)
        self.type = kwargs.get('type', None)
        self.status = kwargs.get('status', None)
        self.memo = kwargs.get('memo', None)
        self.is_retired = kwargs.get('isRetired', None)
        self.id = kwargs.get('id', None)
        self.created_at = kwargs.get('createdAt', None)
        self.roles = kwargs.get('roles', None)
        self.interfaces = kwargs.get('interfaces', None)

    def ip_addr(self):
        pass

    def mac_addr(self):
        pass

