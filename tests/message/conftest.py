"""Unit tests configuration file."""

import pytest

import tests.conftest
from notmuchtask.messages.eml_parser import get_email_parser
from notmuchtask.messages.extract import TextExtractor
from tests.res import get_test_resource


def pytest_configure(config):
    tests.conftest.pytest_configure(config)


@pytest.fixture()
def text_plain__umlauts_email_path():
    return get_test_resource("text_plain", "Umlauts.eml")


@pytest.fixture()
def text_plain__emoji_email_path():
    return get_test_resource("text_plain", "Emoji.eml")


@pytest.fixture()
def text_plain__plaintext_email_path():
    return get_test_resource("text_plain", "ExampleMessage.eml")


@pytest.fixture()
def text_plain__two_recipients():
    return get_test_resource("text_plain", "Two_recipients.eml")


@pytest.fixture()
def multipart__plain_html__apple_mail():
    return get_test_resource("multipart", "MultipartPlainHtml_AppleMail.eml")


@pytest.fixture()
def multipart__chinese_spam():
    return get_test_resource("multipart", "Chinese-Spam.eml")


@pytest.fixture()
def text_extraction():
    return TextExtractor()


@pytest.fixture()
def email_summary_parser():
    return get_email_parser()
