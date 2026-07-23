# learning/code/ex-07-endianness-struct-pack/endianness_pack.py
"""Example 7: Endianness -- Packing 1 as Little-Endian vs. Big-Endian."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import struct  # => co-04: struct's format prefixes ("<", ">") are how Python controls byte order explicitly


def hex_bytes(raw: bytes) -> str:  # => co-04: formats bytes as space-separated hex pairs, easy to eyeball
    """Render bytes as space-separated two-digit hex pairs, e.g. b'\\x01\\x00' -> '01 00'."""  # => co-04: documents hex_bytes's contract -- no runtime output, just sets its __doc__
    return " ".join(f"{byte:02x}" for byte in raw)  # => co-04: one "XX" token per byte, in storage order


if __name__ == "__main__":  # => co-04: entry point -- this block runs only when the file executes directly, not on import
    value = 1  # => co-04: the syllabus's fixed test value -- small enough to make byte order obvious
    little = struct.pack("<i", value)  # => co-04: "<i" = little-endian signed 4-byte int -- LEAST-significant byte first
    big = struct.pack(">i", value)  # => co-04: ">i" = big-endian signed 4-byte int -- MOST-significant byte first
    print(f"little-endian <i: {hex_bytes(little)}")  # => co-04: expect "01 00 00 00" -- the 1 lives in byte 0
    print(f"big-endian    >i: {hex_bytes(big)}")  # => co-04: expect "00 00 00 01" -- the 1 lives in the LAST byte
    assert hex_bytes(little) == "01 00 00 00", "little-endian must place the value byte first"  # => co-04
    assert hex_bytes(big) == "00 00 00 01", "big-endian must place the value byte last"  # => co-04
    assert struct.unpack("<i", little)[0] == value  # => co-04: each byte order decodes back correctly on its OWN
    assert struct.unpack(">i", big)[0] == value  # => co-04: format -- byte order is a pure ENCODING convention
    print("Both orderings verified against the documented patterns: True")  # => co-04: both asserts passed
    # => co-04: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
