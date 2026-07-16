# learning/code/ex-10-codepoint-vs-byte-len/codepoint_vs_byte_len.py
"""Example 10: len(str) vs. len(str.encode('utf-8')) Diverge for Non-ASCII."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


if __name__ == "__main__":  # => co-05: entry point -- this block runs only when the file executes directly, not on import
    samples = ["hello", "café", "文字"]  # => co-05: ASCII, one accented char, two CJK characters
    for s in samples:  # => co-05: one comparison row per sample string
        codepoint_len = len(s)  # => co-05: Python's len() on a str counts UNICODE CODE POINTS, not bytes
        byte_len = len(s.encode("utf-8"))  # => co-05: len() on the encoded bytes counts actual STORAGE bytes
        diverges = codepoint_len != byte_len  # => co-05: True whenever any character needs >1 UTF-8 byte
        print(f"{s!r:<10} codepoints={codepoint_len} utf8-bytes={byte_len} diverges={diverges}")  # => co-05
    ascii_len = len(samples[0])  # => co-05: pure-ASCII case -- every code point IS exactly one byte
    ascii_bytes = len(samples[0].encode("utf-8"))  # => co-05: so these two counts must be EQUAL for ASCII
    assert ascii_len == ascii_bytes, "pure ASCII: codepoint count and byte count must match"  # => co-05
    non_ascii_len = len(samples[1])  # => co-05: "café" has 4 code points
    non_ascii_bytes = len(samples[1].encode("utf-8"))  # => co-05: but 5 bytes -- é alone costs 2 bytes
    assert non_ascii_len != non_ascii_bytes, "non-ASCII: codepoint count and byte count must diverge"  # => co-05
    print(f"ASCII counts match, non-ASCII counts diverge: True")  # => co-05: both asserts passed
    # => co-05: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
