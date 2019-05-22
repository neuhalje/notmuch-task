class TextExtractor(object):
    def __init__(self):

        import html2text

        self._html2markdown = html2text.HTML2Text()
        self._html2markdown.single_line_break = True
        self._html2markdown.unicode_snob = True
        self._html2markdown.ignore_links = True

        self._html2text = html2text.HTML2Text()
        self._html2text.single_line_break = True
        self._html2text.unicode_snob = True

        self._html2text.ignore_links = True
        self._html2text.ignore_emphasis = True
        self._html2text.ignore_images = True
        self._html2text.ignore_tables = True

    def to_plaintext(self, source_mime_type, source_text):
        if source_mime_type == 'text/plain':
            return source_text
        elif source_mime_type == 'text/html':
            return self._html2text.handle(source_text)
        else:
            raise ValueError(
                "Mime type '{}' not supported".format(source_mime_type))

    def to_markdown(self, source_mime_type, source_text):
        if source_mime_type == 'text/plain':
            return source_text
        elif source_mime_type == 'text/html':
            return self._html2markdown.handle(source_text)
        else:
            raise ValueError(
                "Mime type '{}' not supported".format(source_mime_type))
