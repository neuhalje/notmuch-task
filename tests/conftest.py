"""Integration tests configuration file."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

import logging

import pytest


@pytest.fixture()
def sample_msg_primary_key():
    return 'wTG-gncHSu6i-LMHSZ069w'


@pytest.fixture()
def sample_message_id():
    return '<EB8479A4-1C80-427C-B435-56E87C9C2435@example.com>'


@pytest.fixture()
def sample_message_mime_url(sample_msg_primary_key):
    return '/api/v1/messages/by-id/{}/mime'.format(sample_msg_primary_key)


@pytest.fixture()
def sample_message_summary_url(sample_msg_primary_key):
    return '/api/v1/messages/by-id/{}/summary'.format(sample_msg_primary_key)


@pytest.fixture()
def sample_message_upload_url():
    return '/api/v1/messages/upload'


@pytest.fixture()
def sample_message_as_mime():
    return """\
Return-Path: <sender@example.com>
X-Original-To: recipient@example.com
Delivered-To: recipient@example.com
Received: from horstcersior.local.example.com (Horstcersior.local.example.com [172.20.10.125])
	(using TLSv1.2 with cipher ECDHE-RSA-AES256-GCM-SHA384 (256/256 bits))
	(No client certificate requested)
	by mail.example.com (Postfix) with ESMTPSA id 33E5C1C1B8;
	Mon, 23 Oct 2017 15:38:17 +0000 (UTC)
	(envelope-from sender@example.com)
From: Example Sender <sender@example.com>
Content-Type: text/plain
Content-Transfer-Encoding: 7bit
Mime-Version: 1.0 (Mac OS X Mail 11.0 \(3445.1.7\))
Subject: Two recipients
Message-Id: <EB8479A4-1C80-427C-B435-56E87C9C2435@example.com>
Date: Mon, 23 Oct 2017 17:38:22 +0200
To: Example Recipient <recipient@example.com>,
 Another Recipient <another_recipient@example.com>
X-Mailer: Apple Mail (2.3445.1.7)

Body
"""


def pytest_configure(config):
    """Disable verbose output when running tests."""
    logging.basicConfig(level=logging.DEBUG)
