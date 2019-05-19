import logging

import click

from notmuchtask.cli.commands import find_task, find_or_create_task
from notmuchtask.cli.config import get_configuration
from notmuchtask.cli.globals import CONTEXT


@click.group()
@click.option('--debug', is_flag=True, flag_value=True,
              help='Enable debug log.')
@click.option('--configfile', help='Config file.')
def cli(debug: bool, configfile=None, logfile=None):
    if debug:
        logging.basicConfig(filename=logfile, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=logfile, level=logging.INFO)

    CONTEXT.set_config(get_configuration(configfile))


cli.add_command(find_task)
cli.add_command(find_or_create_task)

if __name__ == '__main__':
    cli()
