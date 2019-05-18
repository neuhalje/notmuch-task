# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
# Copyright (c) Jens Neuhalfen

import logging
import os

try:
    # py3k
    import configparser
except ImportError:
    import ConfigParser as configparser

__DEFAULT_CONFIG = """
[tags]
prefix = taskid:                                                                                                                                                            

[taskwarrior]
executable = task
"""

def get_configuration(path=None):
    candidates = [path,
                  os.environ.get('NOTMUCHTASKRC'),
                  os.path.expanduser('~/.notmuchtask.conf')]

    config = configparser.RawConfigParser()
    config.read_string(__DEFAULT_CONFIG, source="<default config>")

    for candidate in candidates:
        if candidate:
            if os.path.isfile(candidate):
                logging.debug("Using config file {}".format(candidate))
                config.read(candidate)
                return config

    return config
