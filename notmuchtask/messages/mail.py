#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys

from notmuchtask.messages.eml_parser import get_email_parser


class MessageMeta(object):
    def __init__(self, message_id, subject):
        if not message_id:
            raise ValueError("No message-id given")

        self.message_id = message_id
        self.subject = subject

        # extract the message ID from notmuch by stripping
        # '<..>' from message id
        if message_id[0] == "<":
            self.nm_message_id = message_id[1:-1]
        else:
            self.nm_message_id = message_id


def _parse_email(message_bytes):
    parser = get_email_parser()
    message = parser.parse_message_bytes(message_bytes)

    subject = message.subject
    message_id = message.message_id
    return MessageMeta(subject=subject, message_id=message_id)


def extract_mail_metadata(message_source):
    if message_source:
        message_source = os.path.expanduser(message_source)
        logging.debug("Parsing message from {}".format(message_source))
        with open(message_source, "rb") as f:
            mail_meta = _parse_email(f.read())
    else:
        logging.debug("Parsing message from stdin")
        mail_meta = _parse_email(sys.stdin.buffer.read())
    return mail_meta
