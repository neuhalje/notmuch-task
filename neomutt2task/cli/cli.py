import logging

import click

from neomutt2task.cli import config, CONTEXT
from neomutt2task.cli.tasks.commands import find_task, find_or_create_task


@click.group()
@click.option('--debug', is_flag=True, flag_value=True, help='Enable debug log.')
@click.option('--configfile', help='Config file.')
def entry_point(debug: bool, configfile=None, logfile=None):
    if debug:
        logging.basicConfig(filename=logfile, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=logfile, level=logging.INFO)

    CONTEXT.set_config(config.get_configuration(configfile))


entry_point.add_command(find_task)
entry_point.add_command(find_or_create_task)

if __name__ == '__main__':
    entry_point()
