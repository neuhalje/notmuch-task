def describe_test_setup():
    def when_unicode_in_sourcecode__correctly_decoded():
        # This does not actually test the app but testsetup
        assert b'\xf0\x9f\x98\x80'.decode("utf-8") == "😀"
        assert b'\xf0\x9f\x92\xa9'.decode("utf-8") == "💩"
