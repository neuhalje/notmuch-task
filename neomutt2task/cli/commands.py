import logging

import click

from neomutt2task import messages, tasks
from neomutt2task.cli.globals import CONTEXT
from neomutt2task.messages.mail import extract_mail_metadata
from neomutt2task.sync import find_task_ids
from neomutt2task.tasks.repository import Task, Taskwarrior



def _find_task(message_source,tag_prefix):
    """
    Finds the taskwarrior task id(s) for a message.
    :param message_source: Path to an email OR None for stdin
    :return: returns all found taskids
    """

    mail_meta = extract_mail_metadata(message_source)

    with  messages.Repository() as message_repo:
        task_ids = find_task_ids(message_repo, mail_meta.nm_message_id, tag_prefix)
        if len(task_ids):
            return task_ids
        else:
            # Message not in the index? Strange
            logging.debug(
                f"""Message with id '{mail_meta.nm_message_id}' either not found in notmuch DB or has no task_id. aborting! """)
            return []



@click.command()
@click.argument('message_source', default=None, required=False)
def find_task(message_source):
    """
    Finds the taskwarrior task id(s) for a message.
    :param message_source: Path to an email OR None for stdin
    :return: prints all found taskids to stdout
    """
    tag_prefix = CONTEXT.config.get("tags", "prefix")
    try:
        task_ids = _find_task(message_source,    tag_prefix)
        if task_ids:
            for task_id in task_ids:
                click.echo(task_id)
        else:
            # Message not in the index? Strange
            exit(1)
    except FileNotFoundError as e:
        click.echo(f"File {message_source} not found!", err=True)
        exit(1)

def _find_or_create_task(message_source, tag_prefix):
    """
    Create a taskwarrior task from a message OR returns the ID(s) of the existing task(s).

    :param message_source: Path to an email OR None for stdin
    :return: list of taskids
    """

    mail_meta = extract_mail_metadata(message_source)

    with messages.Repository() as message_repo:
        task_ids = find_task_ids(message_repo, mail_meta.nm_message_id, tag_prefix)
        if task_ids:
            logging.debug(f"This message already has the following task IDs assigned: {', '.join(task_ids)}")
            # TODO: assert that the task exists
            return task_ids
        else:
            # create a new task
            taskwarrior = Taskwarrior(CONTEXT.config.get("taskwarrior", "executable", fallback="task"))
            with tasks.Repository(taskwarrior) as task_repo:
                new_task = Task.new_task(mail_meta.nm_message_id, mail_meta.subject)
                new_task = task_repo.create_task(new_task)
                message_repo.add_tag(mail_meta.nm_message_id, f"{tag_prefix}{new_task.task_id}")

                return [new_task.task_id]


@click.command()
@click.argument('message_source', default=None, required=False)
def find_or_create_task(message_source):
    """
    Create a taskwarrior task from a message OR returns the IDs of the existing task(s).

    :param message_source: Path to an email OR None for stdin
    :return: prints the task IDs to stdout
    """
    tag_prefix = CONTEXT.config.get("tags", "prefix", fallback="taskid/")

    try:
        for task_id in _find_or_create_task(message_source, tag_prefix):
            click.echo(task_id)
    except FileNotFoundError as e:
        click.echo(f"File {message_source} not found!", err=True)
        exit(1)