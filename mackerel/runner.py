#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    mackerel.runner
    ~~~~~~~~~~~~~~~

    Mackerel client implemented by Python.

    Ported from `mackerel-client-ruby`.
    <https://github.com/mackerelio/mackerel-client-ruby>

    :copyright: (c) 2015 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import logging
import click
from mackerel.client import Client


class Runner(object):

    def __init__(self, verbose=False):
        api_key = os.environ.get('MACKEREL_APIKEY')
        logger = None
        level = logging.INFO
        if verbose is True:
            level = logging.DEBUG

        logging.getLogger('requests').level = logging.ERROR
        logging.basicConfig(level=level, format=Client.debug_log_format)
        logger = logging.getLogger('mackerel.client')

        self.client = Client(mackerel_api_key=api_key, logger=logger)


@click.group()
@click.option('--verbose', default=False, type=click.BOOL)
@click.pass_context
def cli(ctx, verbose):
    runner = Runner(verbose)
    ctx.obj['instance'] = runner


@cli.command()
@click.option('--host-id', default=None)
@click.option('--status', default=None)
@click.pass_context
def status(ctx, host_id, status):
    runner = ctx.obj['instance']
    if status is None:
        if host_id is None:
            data = runner.client.get_hosts()
        else:
            data = [runner.client.get_host(host_id)]
        message = 'name: {0} status: {1} id: {2} roles: {3}'
        for d in data:
            click.echo(message.format(d.name, d.status, d.id, d.roles))
    else:
        runner.client.update_host_status(host_id, status)


@cli.command()
@click.option('--name', default=None)
@click.option('--service', default=None)
@click.option('--role', default=None)
@click.pass_context
def info(ctx, name, service, role):
    runner = ctx.obj['instance']
    data = runner.client.get_hosts(name=name, service=service, role=role)
    [click.echo(host.status) for host in data]


@cli.command()
@click.option('--host-id')
@click.pass_context
def retire(ctx, host_id):
    runner = ctx.obj['instance']
    runner.client.retire_host(host_id)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
