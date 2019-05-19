import logging
import re


class MessageIdNotFoundException(Exception):
    def __init__(self, message_id):
        super().__init__()
        self.message_id = message_id


def find_task_ids(message_repo, nm_message_id, tag_prefix):
    nm_messages = list(
        message_repo.get_messages('id:{}'.format(nm_message_id)))

    if not nm_messages:
        raise MessageIdNotFoundException(nm_message_id)

    task_ids = []

    for nm_message in nm_messages:
        logging.debug(
            "Found a mail '{}'.. looking for tags prefixed with '{}'".format(
                nm_message.get_filename(), tag_prefix))
        nm_tags = nm_message.get_tags()
        for nm_tag in nm_tags:
            logging.debug("Tag: {} ".format(nm_tag))

            match = re.fullmatch(r'{}(.+)'.format(tag_prefix), nm_tag)
            if match:
                logging.debug("Task: {} ".format(match.group(1)))
                task_ids.append(match.group(1))
    return task_ids
