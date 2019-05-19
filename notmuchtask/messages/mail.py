#!/usr/bin/env python
# -*- coding: utf-8 -*-

import email
import logging
import os
import sys


class MessageMeta(object):
    def __init__(self, message_id, subject):
        self.message_id = message_id
        self.subject = subject

        # extract the message ID from notmuch by stripping
        # '<..>' from message id
        if message_id[0] == "<":
            self.nm_message_id = message_id[1:-1]
        else:
            self.nm_message_id = message_id


def _parse_email(src):
    message = email.message_from_file(src)
    subject = message['Subject']
    message_id = message['message-id']
    # FIXME: decode_header notwendig?
    return MessageMeta(subject=subject, message_id=message_id)


def extract_mail_metadata(message_source):
    if message_source:
        message_source = os.path.expanduser(message_source)
        logging.debug("Parsing message from {}".format(message_source))
        with open(message_source, "r") as f:
            mail_meta = _parse_email(f)
    else:
        logging.debug("Parsing message from stdin")
        mail_meta = _parse_email(sys.stdin)
    return mail_meta
