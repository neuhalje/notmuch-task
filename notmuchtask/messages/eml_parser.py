"""Parse .eml files into messages."""

import email
import email.policy
import logging
from pathlib import Path

from notmuchtask.messages.extract import TextExtractor
from .charset_decoder import decode_payload
from .message import Body, MessageSummaryFactory, Address

log = logging.getLogger(__name__)


class MessageParsingError(ValueError):
    pass


def get_email_parser():
    return EmailSummaryParser(
        factory_message_summary=MessageSummaryFactory(TextExtractor()),
        factory_address=Address)


class EmailSummaryParser(object):
    """
    Parse MIME messages into MessageSummary instances.
    """

    def __init__(self, factory_message_summary, factory_address):
        self._factory_message_summary = factory_message_summary
        self._factory_address = factory_address

    def validate_message(self, message):

        # https: // tools.ietf.org / html / rfc822  # section-6.3
        # at least one must be present: FROM / RESENT - FROM / Sender
        has_some_sender = message["From"] \
                          or message["Resent-From"] \
                          or message["Sender"]

        if not has_some_sender:
            raise MessageParsingError(
                "Messages must have at least one of "
                "FROM / RESENT-FROM / Sender")

    def _map_address(self, address_header_address):
        return self._factory_address(
            addr_spec=address_header_address.addr_spec,
            display_name=address_header_address.display_name)

    def _map_addresses(self, address_header):
        if address_header:
            return [self._map_address(addr) for addr in
                    address_header.addresses]
        else:
            return []

    def _parse_message(self, message):
        # Check if any attachments at all
        # if mail.get_content_maintype() != 'multipart':
        #    continue
        #
        message_id = message["Message-Id"]
        rcpt_from = self._map_addresses(message["From"])
        rcpt_to = self._map_addresses(message["To"])
        subject = message["Subject"]
        body = None

        if message.is_multipart():
            for part in message.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))

                # skip any text/plain (txt) attachments
                plain_or_html = (ctype == 'text/plain') or (
                        ctype == 'text/html')
                is_attachment = 'attachment' in cdispo
                if plain_or_html and not is_attachment:
                    part_charset = part.get_param('charset', 'ascii')
                    payload = part.get_payload(decode=True)
                    unicode_body = decode_payload(part_charset, payload)
                    body = Body('text/plain', unicode_body)
                    break
        # not multipart - i.e. plain text, no attachments,
        # keeping fingers crossed
        else:
            message_charset = message.get_param('charset', 'ascii')
            payload = message.get_payload(decode=True)
            unicode_body = decode_payload(message_charset, payload)
            body = Body('text/plain', unicode_body)

        return self._factory_message_summary(message_id=message_id,
                                             rcpt_to=rcpt_to,
                                             rcpt_from=rcpt_from,
                                             subject=subject, bodies=body)

    def parse_message_string(self, message_string):
        """
        Read a MIME message from a string.

        :param message_string: A MIME message as (unicode) string.
        """

        try:
            message = email.message_from_string(
                message_string,
                policy=email.policy.SMTP)

            self.validate_message(message)
            return self._parse_message(message)
        except MessageParsingError as pe:
            raise pe
        except Exception as e:
            raise MessageParsingError(e)

    def parse_message_bytes(self, message_bytes):
        """
        Read a MIME message from a bytes array.

        :param message_bytes: A MIME message as byte array.
        """

        try:
            message = email.message_from_bytes(message_bytes,
                                               policy=email.policy.SMTP)
            self.validate_message(message)
            return self._parse_message(message)
        except MessageParsingError as pe:
            raise pe
        except Exception as e:
            raise MessageParsingError(e)

    def parse_message(self, path):
        """
        Read a MIME message from a path.

        :param path: Path to the message. Must be a file.
        """

        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(
                "Could not resolve '%s' to a file, aborting!" % (path,))

        try:
            with open(path, 'r') as f:
                message = email.message_from_file(f, policy=email.policy.SMTP)
                self.validate_message(message)
                return self._parse_message(message)
        except MessageParsingError as pe:
            raise pe
        except Exception as e:
            raise MessageParsingError(e)
