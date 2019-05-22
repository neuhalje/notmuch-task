import logging
from typing import List

from .extract import TextExtractor

log = logging.getLogger(__name__)


class Address(object):
    def __init__(self, addr_spec, display_name):
        """
        Construct a simple address.

        :param addr_spec: Technical representation of the address.
        "sender@example.com"
        :param display_name: Display name, e.g. "Peter Pan".
        """
        self.addr_spec = addr_spec
        self.display_name = display_name

    def __eq__(self, other):
        if isinstance(other, Address):
            return self.addr_spec == other.addr_spec \
                   and self.display_name == other.display_name
        elif isinstance(other, str):
            # Allow Address objects to be compared to strings
            return self.addr_spec == other
        else:
            return False


class Body(object):
    def __init__(self, mime_type, content):
        """
        Construct a body object.

        :param mime_type: mime type (e.g. text/html or text/plain)
        :param content: The content as string (unicode)
        """
        self.mime_type = mime_type
        self.content = content

    def __eq__(self, other):
        return self.mime_type == other.mime_type \
               and self.content == other.content


class MessageSummaryFactory(object):
    def __init__(self, text_extraction: TextExtractor):
        self._text_extraction = text_extraction

    def __call__(self, *args, **kwargs):
        return MessageSummary(*args, **kwargs,
                              text_extraction=self._text_extraction)


class MessageSummary(object):
    def __init__(self, message_id: str, rcpt_to: List[Address],
                 rcpt_from: List[Address],
                 subject: str, bodies: List[Body], primary_key: str = None,
                 text_extraction=None):
        """
        Construct a simple message.

        :param primary_key: Technical ID of the message
        :param message_id: The message id from the :Message-Id: field
        :param rcpt_to: Recipient of the message. (list)
        :param rcpt_from: Sender of the message. (list)
        :param subject: Subject of the message.
        :param bodies: List of the messages body.
                       The same format must not be present twice.
        """

        self.__MAX_EXCERPT_LEN__ = 120

        def to_list(v):
            if v is None:
                return []
            elif isinstance(v, list):
                return v
            else:
                return [v]

        self._text_extraction = text_extraction
        self.primary_key = primary_key
        self.message_id = message_id
        self.rcpt_to = to_list(rcpt_to)
        self.rcpt_from = to_list(rcpt_from)
        self.subject = subject
        self.body = dict()

        if isinstance(bodies, Body):
            bodies = [bodies]

        if isinstance(bodies, dict):
            for _, body in bodies.items():
                self.body[body['mime_type']] = body
        else:
            for body in bodies or []:
                if body.mime_type in self.body:
                    raise ValueError(
                        "mime type {} passed twice!".format(body.mime_type))
                self.body[body.mime_type] = body

    @property
    def plaintext_body(self):
        if 'text/plain' in self.body:
            return self.body['text/plain'].content
        elif 'text/html' in self.body:

            html_body = self.body['text/html'].content

            return self._text_extraction.to_plaintext('text/html', html_body)
        else:
            return ""

    @property
    def markdown_body(self):
        if 'text/plain' in self.body:
            return self.body['text/plain'].content
        elif 'text/html' in self.body:

            html_body = self.body['text/html'].content

            return self._text_extraction.to_markdown('text/html', html_body)
        else:
            return ""

    def __eq__(self, other):
        return self.message_id == other.message_id \
               and self.rcpt_to == other.rcpt_to \
               and self.rcpt_from == other.rcpt_from \
               and self.subject == other.subject \
               and self.body == other.body
