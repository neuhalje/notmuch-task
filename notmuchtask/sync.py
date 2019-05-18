import logging
import re


def find_task_ids(message_repo, nm_message_id, tag_prefix):
    nm_messages = list(message_repo.get_messages(f'id:{nm_message_id}'))
    task_ids = []

    for nm_message in nm_messages:
        logging.debug(f"Found a mail '{nm_message.get_filename()}'.. looking for tags prefixed with '{tag_prefix}'")
        nm_tags = nm_message.get_tags()
        for nm_tag in nm_tags:
            logging.debug(f"Tag: {nm_tag} ")

            match = re.fullmatch(rf'{tag_prefix}(.+)', nm_tag)
            if match:
                logging.debug(f"Task: {match[1]} ")
                task_ids.append(match[1])
    return task_ids
