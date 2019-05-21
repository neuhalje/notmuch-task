# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison
# pylint: disable=line-too-long,bad-continuation

from pytest import raises

from notmuchtask.messages.eml_parser import MessageParsingError
from tests.res import get_test_resource


def describe_parse_function():
    def when_no_valid_path__fails(email_summary_parser):
        with raises(FileNotFoundError,
                    match="Could not resolve '[^']+' to a file, aborting!"):
            email_summary_parser.parse_message("/non/existing/path")

    def when_no_path__fails(email_summary_parser):
        with raises(FileNotFoundError,
                    match="Could not resolve '' to a file, aborting!"):
            email_summary_parser.parse_message("")

    def when_valid_path__returns_something(email_summary_parser,
                                           text_plain__plaintext_email_path):
        assert email_summary_parser.parse_message(
            text_plain__plaintext_email_path) is not None


def describe_messages_must_have_sender():
    def from_present__parses(email_summary_parser):
        # https: // tools.ietf.org / html / rfc822  # section-6.3
        # FROM / RESENT - FROM / Sender : at least one must be present
        message = "From: <sender@example.com>"
        assert email_summary_parser.parse_message_string(message) is not None

    def sender_present__parses(email_summary_parser):
        # https: // tools.ietf.org / html / rfc822  # section-6.3
        # FROM / RESENT - FROM / Sender : at least one must be present
        message = "Sender: <sender@example.com>"
        assert email_summary_parser.parse_message_string(message) is not None

    def resent_from_present__parses(email_summary_parser):
        # https: // tools.ietf.org / html / rfc822  # section-6.3
        # FROM / RESENT - FROM / Sender : at least one must be present
        message = "Resent-From: <sender@example.com>"
        assert email_summary_parser.parse_message_string(message) is not None

    def no_sender__fails(email_summary_parser):
        # https: // tools.ietf.org / html / rfc822  # section-6.3
        # FROM / RESENT - FROM / Sender : at least one must be present
        message = "Subject: Fail"
        with raises(MessageParsingError):
            email_summary_parser.parse_message_string(message)


def describe_plaintext_messages():
    def when_text_plain_message__reads_message_id(email_summary_parser,
                                                  text_plain__plaintext_email_path):
        message = email_summary_parser.parse_message(
            text_plain__plaintext_email_path)
        assert message.message_id == "<A3E89D52-C626-42DF-873F-F0181A08C7F6@example.com>"

    def when_text_plain_message__reads_mail_body(email_summary_parser,
                                                 text_plain__plaintext_email_path):
        message = email_summary_parser.parse_message(
            text_plain__plaintext_email_path)

        assert message.body['text/plain'].mime_type == "text/plain"
        assert message.body['text/plain'].content == """Lorem ipsum dolor sit amet, consectetur \
adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut \
enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea \
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate \
velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non \
proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    def when_text_plain_message__reads_mail_subject(email_summary_parser,
                                                    text_plain__plaintext_email_path):
        message = email_summary_parser.parse_message(
            text_plain__plaintext_email_path)
        assert message.subject == "Example Message"

    def when_text_plain_message__reads_mail_recipient(email_summary_parser,
                                                      text_plain__plaintext_email_path):
        message = email_summary_parser.parse_message(
            text_plain__plaintext_email_path)
        assert len(message.rcpt_to) == 1
        assert next(addr.addr_spec for addr in
                    message.rcpt_to) == "recipient@example.com"

    def when_text_plain_message__reads_mail_sender(email_summary_parser,
                                                   text_plain__plaintext_email_path):
        message = email_summary_parser.parse_message(
            text_plain__plaintext_email_path)
        assert len(message.rcpt_from) == 1
        assert "sender@example.com" in message.rcpt_from

    def when_emoji_message__reads_body(email_summary_parser,
                                       text_plain__emoji_email_path):
        message = email_summary_parser.parse_message(
            text_plain__emoji_email_path)
        assert message.body['text/plain'].mime_type == "text/plain"
        assert message.body['text/plain'].content == """poop:💩
smiley:😀"""

    def when_umlaut_message__reads_body(email_summary_parser,
                                        text_plain__umlauts_email_path):
        message = email_summary_parser.parse_message(
            text_plain__umlauts_email_path)
        assert message.body['text/plain'].mime_type == "text/plain"
        assert message.body['text/plain'].content == """äöüÄÖÜ"""

    def when_umlaut_message__reads_subject(email_summary_parser,
                                           text_plain__umlauts_email_path):
        message = email_summary_parser.parse_message(
            text_plain__umlauts_email_path)
        assert message.subject == """Umlauts: äöü"""

    def when_two_recipients__both_are_found(email_summary_parser,
                                            text_plain__two_recipients):
        message = email_summary_parser.parse_message(
            text_plain__two_recipients)
        assert "recipient@example.com" in message.rcpt_to
        assert "another_recipient@example.com" in message.rcpt_to


def describe_multipart_messages():
    def when_text_plain__and_html_message__reads_mail_body_for_text(
            email_summary_parser,
            multipart__plain_html__apple_mail):
        message = email_summary_parser.parse_message(
            multipart__plain_html__apple_mail)

        assert message.body['text/plain'].mime_type == "text/plain"
        assert message.body['text/plain'].content == """italic
underline
bold
red

"""

        def when_text_plain__and_html_message__reads_mail_body_for_html(
                email_summary_parser,
                multipart__plain_html__apple_mail):
            message = email_summary_parser.parse_message(
                multipart__plain_html__apple_mail)

            assert message.body['text/html'].mime_type == "text/html"
            assert message.body['text/html'].content == """\
<html><head><meta http-equiv="Content-Type" content="text/html; charset=us-ascii"></head><body \
style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" \
class=""><i class="">italic</i><div class=""><u class="">underline</u></div><div class=""><b \
class="">bold</b></div><div class=""><font color="#ff2600" class="">red</font></div><div \
class=""><br class=""></div></body></html>\
"""

    def when_text_plain__and_html_message__reads_mail_subject(
            email_summary_parser,
            multipart__plain_html__apple_mail):
        message = email_summary_parser.parse_message(
            multipart__plain_html__apple_mail)
        assert message.subject == "Formatted text (RTF)"

    def when_text_plain__and_html_message__reads_mail_recipient(
            email_summary_parser,
            multipart__plain_html__apple_mail):
        message = email_summary_parser.parse_message(
            multipart__plain_html__apple_mail)

        assert "recipient@example.com" in message.rcpt_to
        assert len(message.rcpt_to) == 1

    def when_text_plain__and_html_message__reads_mail_sender(
            email_summary_parser,
            multipart__plain_html__apple_mail):
        message = email_summary_parser.parse_message(
            multipart__plain_html__apple_mail)

        assert "sender@example.com" in message.rcpt_from
        assert len(message.rcpt_from) == 1

    def when_unicode_chinese_spam__decoded(email_summary_parser,
                                           multipart__chinese_spam):
        message = email_summary_parser.parse_message(multipart__chinese_spam)

        assert "sender@example.com" in message.rcpt_from
        assert len(message.rcpt_from) == 1

        assert message.subject == "保护固定资产的安全完整，实现资产的保值增值"
        assert message.body["text/plain"].mime_type == "text/plain"
        assert "固定资产是企业重要" in message.body["text/plain"].content


def describe_problem_messages():
    def _message_path(message_name):
        return get_test_resource("problem_cases", message_name)

    def when_multipart_encoded_latin1_body_gets_decoded(email_summary_parser):
        path = _message_path("multipart__encoded_latin1.eml")
        message = email_summary_parser.parse_message(path)
        assert message is not None

    def when_text_plain__encoded_iso_8859_1_body_gets_decoded(
            email_summary_parser):
        path = _message_path("text_plain__encoded_iso-8859-1.eml")
        message = email_summary_parser.parse_message(path)
        assert message is not None

    def when_html_only__body_gets_decoded(email_summary_parser):
        path = _message_path("html_body_only.eml")
        message = email_summary_parser.parse_message(path)
        assert message is not None

    def when_body_violates_transfer_encoding__body_gets_decoded_with_best_effort(
            email_summary_parser):
        """
        Some MUAs set content-encoding wrong. Heuristics should figure out the correct value.
        """
        path = _message_path("violating_7bit_transfer_encoding.eml")
        message = email_summary_parser.parse_message(path)
        assert message is not None
        assert message.body[
                   'text/plain'].content == "The next character will be a violation of 7bit " \
                                            "transfer encoding: Ä"

    def when_message_no_body_only_attachment__no_bodies_found(
            email_summary_parser):
        path = _message_path("message_no_body_only_attachment.eml")
        message = email_summary_parser.parse_message(path)
        assert message is not None
        assert message.body is not None
        assert len(message.body) == 0

    def when_message_has_no_to__parsing_succeeds(email_summary_parser):
        path = _message_path("no_to_field.eml")
        message = email_summary_parser.parse_message(path)
        assert message is not None
        assert message.rcpt_from is not None
        assert message.rcpt_to == []
