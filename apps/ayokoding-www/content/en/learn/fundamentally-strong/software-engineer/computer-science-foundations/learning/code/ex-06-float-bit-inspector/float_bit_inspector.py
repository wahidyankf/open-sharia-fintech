# learning/code/ex-06-float-bit-inspector/float_bit_inspector.py
"""Example 6: IEEE-754 Float-Bit Inspector -- Decoding 1.0's Sign/Exponent/Mantissa."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import struct  # => co-03: struct.pack/unpack is the stdlib bridge between a Python float and its raw bytes
from typing import NamedTuple  # => co-03: typing import supporting the typed structures below


class Ieee754Fields(NamedTuple):  # => co-03: the three fields IEEE 754-2019 binary64 packs into 64 bits
    sign: int  # => co-03: bit 63 -- 0 for positive, 1 for negative
    exponent: int  # => co-03: bits 62-52 (11 bits), stored with a bias of 1023
    mantissa: int  # => co-03: bits 51-0 (52 bits) -- the fractional part of the significand


def inspect(x: float) -> Ieee754Fields:  # => co-03: decomposes a float into its raw IEEE-754 bit fields
    """Decompose a float into its IEEE-754 binary64 sign/exponent/mantissa fields."""  # => co-03: documents inspect's contract -- no runtime output, just sets its __doc__
    raw = struct.pack(">d", x)  # => co-03: 8 bytes, big-endian ("> d" = big-endian double) -- MSB first
    bits = int.from_bytes(raw, byteorder="big")  # => co-03: the 8 bytes as one 64-bit unsigned integer
    sign = (bits >> 63) & 0x1  # => co-03: shift the top bit down, mask to 1 bit
    exponent = (bits >> 52) & 0x7FF  # => co-03: next 11 bits, masked -- still BIASED (add -1023 to unbias)
    mantissa = bits & 0xFFFFFFFFFFFFF  # => co-03: the low 52 bits -- the stored fractional significand
    return Ieee754Fields(sign, exponent, mantissa)  # => co-03: returns this computed value to the caller


def reconstruct(fields: Ieee754Fields) -> float:  # => co-03: fields -> float, proving the decode round-trips
    """Rebuild a float from its decoded sign/exponent/mantissa fields."""  # => co-03: documents reconstruct's contract -- no runtime output, just sets its __doc__
    bits = (fields.sign << 63) | (fields.exponent << 52) | fields.mantissa  # => co-03: reassemble the 64 bits
    raw = bits.to_bytes(8, byteorder="big")  # => co-03: back to 8 raw bytes, same big-endian order as inspect()
    return struct.unpack(">d", raw)[0]  # => co-03: unpack() is the exact inverse of pack() above


if __name__ == "__main__":  # => co-03: entry point -- this block runs only when the file executes directly, not on import
    x = 1.0  # => co-03: the syllabus's fixed test value -- a value with a clean, easy-to-verify encoding
    fields = inspect(x)  # => co-03: decode 1.0's raw bit layout
    print(f"sign={fields.sign} exponent={fields.exponent} (biased) mantissa={fields.mantissa}")  # => co-03
    unbiased_exponent = fields.exponent - 1023  # => co-03: IEEE 754-2019's fixed bias for binary64 is 1023
    print(f"unbiased exponent = {unbiased_exponent}")  # => co-03: expect 0 -- 1.0 = 1.0 * 2**0
    assert fields.sign == 0, "1.0 is positive -- sign bit must be 0"  # => co-03
    assert fields.exponent == 1023, "1.0's biased exponent must be exactly 1023 (unbiased 0)"  # => co-03
    assert fields.mantissa == 0, "1.0's mantissa is all zero -- an EXACT power of two"  # => co-03
    rebuilt = reconstruct(fields)  # => co-03: decode then re-encode -- must recover the original float exactly
    print(f"reconstructed = {rebuilt!r}")  # => co-03: prints the round-tripped value
    assert rebuilt == x, "decoded fields must reconstruct to the original 1.0"  # => co-03: exact round-trip
    print(f"Round-trip matches original 1.0: True")  # => co-03: reached only if every assert above passed
    # => co-03: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
