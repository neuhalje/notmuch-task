# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) Jens Neuhalfen

from __future__ import print_function, absolute_import, unicode_literals

import logging
import os

try:
    # py3k
    import configparser
except ImportError:
    import ConfigParser as configparser


def get_configuration(path=None):
    candidates = [path,
                  os.environ.get('NEOMUTT2TASKRC'),
                  os.path.expanduser('~/.neomutt2task.conf')]

    config = configparser.RawConfigParser()

    for candidate in candidates:
        if candidate:
            if os.path.isfile(candidate):
                logging.debug(f"Using config file {candidate}")
                config.read(candidate)
                return config
    config.add_section("tags")
    config.set("tags", "prefix", "taskid:")
    return config
