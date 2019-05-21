# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison
# pylint: disable=line-too-long,bad-continuation
from notmuchtask.messages.message import Body, MessageSummary

text_plain_body = """italic

underline

bold

red

"""

text_html_body = """\
<html><head><meta http-equiv="Content-Type" content="text/html; charset=us-ascii"></head><body \
style="word-wrap: break-word; -webkit-nbsp-mode: space; line-break: after-white-space;" \
class=""><i class="">italic</i><div class=""><u class="">underline</u></div><div class=""><b \
class="">bold</b></div><div class=""><font color="#ff2600" class="">red</font></div><div \
class=""></body></html>\
"""

# This is a rather bad test because it depends on text2html behavior
text_stripped_html_body = """_italic_

 _underline_

 **bold**

red

"""

text_rtf_body = r"""{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf200
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red251\green2\blue7;}
{\*\expandedcolortbl;;\cssrgb\c100000\c14913\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww12600\viewh7800\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803
\pardirnatural\partightenfactor0

\f0\i\fs24 \cf0 italic
\i0 \
\ul underline\ulnone \

\b bold
\b0 \
\cf2 red}"""


def __plain_text_body(text=text_plain_body):
    return Body("text/plain", text)


def __html_body(text=text_html_body):
    return Body("text/html", text)


def __rtf_body(text=text_rtf_body):
    return Body("text/rtf", text)


def __msg(text_extraction, bodies):
    return MessageSummary("noid", [], [], "no subject", bodies,
                          text_extraction=text_extraction)


def describe_text_body():
    def when_has_text_body__text_is_returned(text_extraction):
        msg = __msg(text_extraction, [__plain_text_body()])

        assert text_plain_body == msg.plaintext_body
        assert text_plain_body == msg.markdown_body

    def when_has_html_body__text_is_returned(text_extraction):
        """
        This test is a bit faulty because it also tests html2text
        """
        msg = __msg(text_extraction, [__html_body()])
        assert text_plain_body == msg.plaintext_body
        assert text_stripped_html_body == msg.markdown_body

    def when_has_multiple_with_text_body__text_is_returned(text_extraction):
        msg = __msg(text_extraction, [__html_body(), __plain_text_body()])

        assert text_plain_body == msg.plaintext_body

    def when_has_no_body__returns_empty_string(text_extraction):
        msg = __msg(text_extraction, [])
        assert "" == msg.plaintext_body

    def when_has_no_rtf_body__returns_empty_string(text_extraction):
        msg = __msg(text_extraction, [__rtf_body()])
        assert "" == msg.plaintext_body

    def when_has_no_understandable_body__returns_empty_string(text_extraction):
        msg = __msg(text_extraction, [Body("text/binary", "xxx")])
        assert "" == msg.plaintext_body
