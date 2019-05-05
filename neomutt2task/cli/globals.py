from configparser import RawConfigParser


class Context(object):
    def set_config(self, config: RawConfigParser):
        self.config = config

CONTEXT = Context()
