def decode_payload(advised_charset, payload):
    def try_decode(charset):
        try:
            return True, payload.decode(charset, "strict")
        except UnicodeDecodeError:
            return False, None

    encodings = [advised_charset, "ascii", "utf-8", "iso-8859-15",
                 "iso-8859-1", "latin1",
                 "Windows-1252"]
    for encoding in encodings:
        success, result = try_decode(encoding)
        if success:
            return result
