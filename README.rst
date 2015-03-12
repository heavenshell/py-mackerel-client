mackerel.client
===============
.. image:: https://travis-ci.org/heavenshell/py-mackerel-client.svg?branch=master
    :target: https://travis-ci.org/heavenshell/py-mackerel-client

mackerel.client is a python library to access Mackerel (https://mackerel.io/).

This client is Ported from `mackerel-client-ruby <https://github.com/mackerelio/mackerel-client-ruby>`_.

Install
-------

.. code:: shell

  $ pip install mackerel.client


Dependency
----------

mackerel.client use `requests <http://docs.python-requests.org/en/latest/>`_, `simplejson <https://github.com/simplejson/simplejson>`_ and `click <http://click.pocoo.org/3/>`_.

Usage
-----
Get hosts
~~~~~~~~~

.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key')
  host = client.get_hosts()


Get host
~~~~~~~~

.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key')
  host = client.get_host('<hostId>')


Update host status
~~~~~~~~~~~~~~~~~~

.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key')
  # Poweroff.
  self.client.update_host_status('<hostId>', 'poweroff')
  # Standby.
  self.client.update_host_status('<hostId>', 'standby')
  # Working.
  self.client.update_host_status('<hostId>', 'working')
  # Maintenance.
  self.client.update_host_status('<hostId>', 'maintenance')

Retire host
~~~~~~~~~~~

.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key')
  self.client.retire_host('<hostId>')


Get latest metrics
~~~~~~~~~~~~~~~~~~

.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key')
  # Get hostId A's and hostId B's loadavg5, memory.free value.
  metrics = self.client.get_latest_metrics(['<hostId A>', '<hostId B>'],
                                           ['loadavg5', 'memory.free'])



Post metrics
~~~~~~~~~~~~
.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key>')
  metrics = [
      {
          'hostId': '<hostId>', 'name': 'custom.metrics.loadavg',
          'time': 1401537844, 'value': 1.4
      },
      {
          'hostId': '<hostId>', 'name': 'custom.metrics.uptime',
          'time': 1401537844, 'value': 500
      }

  ]
  # Post `custom.metrics.loadavg` and `custom.metrics.uptime` to `hostId`.
  client.post_metrics(metrics)


Post service metrics
~~~~~~~~~~~~~~~~~~~~
.. code:: python

  from mackerel.client import Client

  client = Client(mackerel_api_key='<Put your API key>')
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
  # Post 'custom.metrics.latency' and 'custom.metrics.uptime' to `service_name`.
  self.client.post_service_metrics('service_name', metrics)


CLI
---

Get host(s) information from hostname or service, role.

.. code:: shell

  $ mkr.py info [--name foo] [--service service] [--role role]

Set status of a host.

.. code:: shell

  $ mkr.py status --host-id foo --status working

Retire a host.

.. code:: shell

  $ mkr.py retire --host-id foo

Get status of a host.

.. code:: shell

  $ mkr.py status --host-id foo

Authentication
--------------

.. code:: shell

  $ export MACKEREL_APIKEY=foobar

