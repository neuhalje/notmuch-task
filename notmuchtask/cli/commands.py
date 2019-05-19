import logging

import click

from notmuchtask import messages, tasks
from notmuchtask.cli.exitcodes import EXIT_GENERAL_ERROR, \
    EXIT_FILE_NOT_FOUND, \
    EXIT_TASK_NOT_FOUND, \
    EXIT_MESSAGE_NOT_FOUND_IN_NOTMUCH
from notmuchtask.cli.globals import CONTEXT
from notmuchtask.messages.mail import extract_mail_metadata
from notmuchtask.sync import find_task_ids, MessageIdNotFoundException
from notmuchtask.tasks.repository import Task, Taskwarrior


def __exit_ok():
    exit(0)


def __exit_general_error(e):
    click.echo("Unexpected error!", err=True)
    logging.exception(e)
    exit(EXIT_GENERAL_ERROR)


def __exit_file_not_found(filename):
    click.echo("File '{}'' not found!".format(filename), err=True)
    exit(EXIT_FILE_NOT_FOUND)


def __exit_task_not_found(message_id):
    click.echo("No task for '{}'' found!".format(message_id), err=True)
    exit(EXIT_TASK_NOT_FOUND)


def __exit_message_not_found_in_notmuch(message_id):
    click.echo("Messageid '{}'' not found in notmuch!".format(message_id),
               err=True)
    exit(EXIT_MESSAGE_NOT_FOUND_IN_NOTMUCH)


def _find_task(message_source, tag_prefix):
    """
    Finds the taskwarrior task id(s) for a message.

    :exception MessageIdNotFoundException: message id not found in notmuch
    :param message_source: Path to an email OR None for stdin
    :return: returns all found taskids
    """

    mail_meta = extract_mail_metadata(message_source)

    with messages.Repository() as message_repo:
        task_ids = find_task_ids(message_repo, mail_meta.nm_message_id,
                                 tag_prefix)
        if len(task_ids):
            return task_ids
        else:
            logging.debug(
                """Message with id '{}' has no task_id""".format(
                    mail_meta.nm_message_id))
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
        task_ids = _find_task(message_source, tag_prefix)
        if task_ids:
            for task_id in task_ids:
                click.echo(task_id)
        else:
            # Message not in the index? Strange
            __exit_task_not_found(message_source)
    except FileNotFoundError:
        __exit_file_not_found(message_source)
    except MessageIdNotFoundException as e:
        __exit_message_not_found_in_notmuch(e.message_id)
    except Exception as e:
        __exit_general_error(e)


def _find_or_create_task(message_source, tag_prefix):
    """
    Create a taskwarrior task from a message OR returns the ID(s) of the
    existing task(s).

    :param message_source: Path to an email OR None for stdin
    :return: list of taskids
    """

    mail_meta = extract_mail_metadata(message_source)

    with messages.Repository() as message_repo:
        task_ids = find_task_ids(message_repo, mail_meta.nm_message_id,
                                 tag_prefix)
        if task_ids:
            logging.debug(
                "This message already has the following task IDs assigned: {}"
                .format(', '.join(task_ids)))
            # TODO: assert that the task exists
            return task_ids
        else:
            # create a new task
            taskwarrior = Taskwarrior(
                CONTEXT.config.get("taskwarrior", "executable"))
            with tasks.Repository(taskwarrior) as task_repo:
                new_task = Task.new_task(mail_meta.nm_message_id,
                                         mail_meta.subject)
                new_task = task_repo.create_task(new_task)
                message_repo.add_tag(mail_meta.nm_message_id,
                                     "{}{}".format(tag_prefix,
                                                   new_task.task_id))

                return [new_task.task_id]


@click.command()
@click.argument('message_source', default=None, required=False)
def find_or_create_task(message_source):
    """
    Returns the ID of the task, creates one if needed.

    Create a taskwarrior task from a message OR returns the IDs of the
    existing task(s).

    :param message_source: Path to an email OR None for stdin
    :return: prints the task IDs to stdout
    """
    tag_prefix = CONTEXT.config.get("tags", "prefix")

    try:
        for task_id in _find_or_create_task(message_source, tag_prefix):
            click.echo(task_id)
    except FileNotFoundError:
        __exit_file_not_found(message_source)
    except MessageIdNotFoundException as e:
        __exit_message_not_found_in_notmuch(e.message_id)
    except Exception as e:
        __exit_general_error(e)
