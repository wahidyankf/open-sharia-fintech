# learning/code/ex-09-utf8-encode-multibyte/utf8_encode.py
"""Example 9: UTF-8 Multi-Byte Encoding -- an Accented Letter and a CJK Character."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


if __name__ == "__main__":  # => co-05: entry point -- this block runs only when the file executes directly, not on import
    word = "café"  # => co-05: the final character is U+00E9 LATIN SMALL LETTER E WITH ACUTE
    kanji = "文"  # => co-05: U+6587, a single CJK ideograph (means "script"/"writing")
    encoded_word = word.encode("utf-8")  # => co-05: RFC 3629's variable-length, ASCII-compatible encoding
    encoded_kanji = kanji.encode("utf-8")  # => co-05: the same encoding applied to a higher code point
    accented_char_bytes = "é".encode("utf-8")  # => co-05: encode JUST "é" in isolation for an exact byte count
    print(f"'café'.encode('utf-8') = {encoded_word!r} ({len(encoded_word)} bytes total)")  # => co-05
    print(f"'é' alone encodes to {accented_char_bytes!r} ({len(accented_char_bytes)} bytes)")  # => co-05
    print(f"'文'.encode('utf-8') = {encoded_kanji!r} ({len(encoded_kanji)} bytes)")  # => co-05
    assert len(accented_char_bytes) == 2, "é (U+00E9) must encode to exactly 2 UTF-8 bytes"  # => co-05
    assert len(encoded_kanji) == 3, "文 (U+6587) must encode to exactly 3 UTF-8 bytes"  # => co-05
    print(f"é is 2 bytes, 文 is 3 bytes: True")  # => co-05: reached only if both length asserts passed
    # => co-05: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
