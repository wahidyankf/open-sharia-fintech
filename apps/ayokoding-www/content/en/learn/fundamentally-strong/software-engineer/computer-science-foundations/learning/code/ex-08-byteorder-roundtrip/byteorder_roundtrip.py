# learning/code/ex-08-byteorder-roundtrip/byteorder_roundtrip.py
"""Example 8: Byte-Order Round-Trip -- sys.byteorder and int.to_bytes/from_bytes."""  # => co-04: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import sys  # => co-04: sys.byteorder reports THIS interpreter's native platform byte order


if __name__ == "__main__":  # => co-04: entry point -- this block runs only when the file executes directly, not on import
    print(f"sys.byteorder (this platform's native order) = {sys.byteorder!r}")  # => co-04: "little" on x86/ARM
    value = 4_660  # => co-04: 0x1234 -- two distinct nonzero bytes make byte order visible in the hex dump
    for order in ("little", "big"):  # => co-04: round-trip through BOTH orders, not just the native one
        encoded = value.to_bytes(2, byteorder=order)  # => co-04: encode as exactly 2 bytes in this order # type: ignore[arg-type]
        decoded = int.from_bytes(encoded, byteorder=order)  # => co-04: decode with the SAME order used to encode # type: ignore[arg-type]
        print(f"{order:<6}: encoded={encoded.hex()} decoded={decoded}")  # => co-04: shows both bytes and the value
        assert decoded == value, f"{order}-endian round-trip must recover the original value"  # => co-04
    little_bytes = value.to_bytes(2, byteorder="little").hex()  # => co-04: e.g. "3412" -- low byte 0x34 first
    big_bytes = value.to_bytes(2, byteorder="big").hex()  # => co-04: e.g. "1234" -- high byte 0x12 first
    print(f"little bytes = {little_bytes}, big bytes = {big_bytes}")  # => co-04: same value, different byte layout
    assert little_bytes != big_bytes, "the two orders must produce genuinely different byte layouts"  # => co-04
    print("Round-trip identity holds for both orders: True")  # => co-04: reached only if every assert passed
    # => co-04: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
