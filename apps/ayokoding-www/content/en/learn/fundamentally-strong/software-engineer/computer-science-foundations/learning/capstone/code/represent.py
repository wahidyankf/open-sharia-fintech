# learning/capstone/code/represent.py
"""Capstone Step 1: an int/float <-> binary/hex converter, plus an IEEE-754 float-bit inspector.

Ties together co-01 (positional number systems), co-02 (two's complement), and co-03 (IEEE-754
floats) into one small, reusable "representation toolkit" -- the same primitives Examples 1, 3,
and 6 introduced separately, now packaged as functions a caller can import and reuse directly.
"""  # => co-01: this file's own restated purpose, doubling as its module __doc__
# => co-01: no runtime output beyond setting __doc__ -- the three paragraphs above just orient the reader

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import struct  # => co-03: struct.pack/unpack -- the bridge between a Python float and its raw IEEE-754 bytes
from typing import NamedTuple  # => co-03: typing import supporting the typed structures below


def int_to_binary(n: int) -> str:  # => co-01: positional-system conversion, unsigned magnitude only
    """Convert a non-negative int to its binary string (no '0b' prefix)."""  # => co-01: this file's own restated purpose, doubling as its module __doc__
    if n < 0:  # => co-01: this function's contract is unsigned -- negative ints need to_twos_complement below
        raise ValueError("int_to_binary expects a non-negative int -- use to_twos_complement for negatives")  # => co-01: continues the statement started above
    return bin(n)[2:] if n else "0"  # => co-01: bin() does the division-by-2 conversion; strip its "0b" prefix


def int_to_hex(n: int) -> str:  # => co-01: the SAME value, rendered in base 16 instead of base 2
    """Convert a non-negative int to its hex string (no '0x' prefix)."""  # => co-01: documents int_to_hex's contract -- no runtime output, just sets its __doc__
    return hex(n)[2:] if n else "0"  # => co-01: hex() does the division-by-16 conversion; strip its "0x" prefix


def to_twos_complement(n: int, bits: int = 8) -> str:  # => co-02: signed int -> fixed-width two's-complement bits
    """Render a signed int in `bits`-wide two's complement."""  # => co-02: documents to_twos_complement's contract -- no runtime output, just sets its __doc__
    mask = (1 << bits) - 1  # => co-02: keeps only the low `bits` bits -- Python's arbitrary-precision AND does the encoding
    return format(n & mask, f"0{bits}b")  # => co-02: zero-padded binary string, exactly `bits` characters wide


class Ieee754Fields(NamedTuple):  # => co-03: the three fields IEEE 754-2019 binary64 packs into 64 bits
    sign: int  # => co-03: bit 63 -- 0 positive, 1 negative
    exponent: int  # => co-03: bits 62-52 (11 bits), BIASED by 1023
    mantissa: int  # => co-03: bits 51-0 (52 bits) -- the stored fractional significand


def inspect_float(x: float) -> Ieee754Fields:  # => co-03: decomposes a float into its raw IEEE-754 bit fields
    """Decompose a float into its IEEE-754 binary64 sign/exponent/mantissa fields."""  # => co-03: documents inspect_float's contract -- no runtime output, just sets its __doc__
    bits = int.from_bytes(struct.pack(">d", x), byteorder="big")  # => co-03: 8 big-endian bytes -> one 64-bit int
    return Ieee754Fields(  # => co-03: mask/shift out each field from the packed 64-bit integer
        sign=(bits >> 63) & 0x1,  # => co-03: the top bit
        exponent=(bits >> 52) & 0x7FF,  # => co-03: the next 11 bits
        mantissa=bits & 0xFFFFFFFFFFFFF,  # => co-03: the low 52 bits
    )  # => co-03: closes the multi-line construct opened above


def float_bits_string(x: float) -> str:  # => co-03: the full 64-bit pattern, grouped for readability
    """Render x's IEEE-754 binary64 bit pattern as sign|exponent|mantissa, space-separated."""  # => co-03: documents float_bits_string's contract -- no runtime output, just sets its __doc__
    f = inspect_float(x)  # => co-03: decode the three fields
    return f"{f.sign:01b} {f.exponent:011b} {f.mantissa:052b}"  # => co-03: 1 + 11 + 52 = 64 bits total


def demonstrate_rounding_error() -> tuple[float, bool]:  # => co-03: the structural (not buggy) 0.1+0.2 fact
    """Return (0.1 + 0.2, whether it equals 0.3) -- IEEE-754 rounding is structural, not a bug."""  # => co-03: documents demonstrate_rounding_error's contract -- no runtime output, just sets its __doc__
    total = 0.1 + 0.2  # => co-03: neither 0.1 nor 0.2 has an exact binary64 representation -- both already round
    return total, total == 0.3  # => co-03: the sum and whether it happens to equal the (also-rounded) literal 0.3


if __name__ == "__main__":  # => co-03: entry point -- this block runs only when the file executes directly, not on import
    print("=== base conversion ===")  # => co-01: section 1 of the toolkit demo
    value = 156  # => co-01: the same fixed test value Example 1 used, for continuity
    print(f"{value} -> binary {int_to_binary(value)}, hex {int_to_hex(value)}")  # => co-01: both conversions shown
    assert int_to_binary(value) == "10011100", "must match the known bit pattern for 156"  # => co-01
    assert int(int_to_binary(value), 2) == value == int(int_to_hex(value), 16), "round-trip must recover 156"  # => co-01

    print("\n=== two's complement ===")  # => co-02: section 2 of the toolkit demo
    negative = -42  # => co-02: the same fixed test value Example 3 used
    print(f"{negative} in 8-bit two's complement = {to_twos_complement(negative)}")  # => co-02
    assert to_twos_complement(negative) == "11010110", "must match the known 8-bit pattern for -42"  # => co-02

    print("\n=== IEEE-754 float inspection ===")  # => co-03: section 3 of the toolkit demo
    known_value = 1.0  # => co-03: a float with a clean, easy-to-verify encoding
    print(f"float_bits(1.0)  = {float_bits_string(known_value)}")  # => co-03: sign|exponent|mantissa, grouped
    fields = inspect_float(known_value)  # => co-03: decode 1.0's fields directly, for the exact-match assertions
    assert fields == Ieee754Fields(sign=0, exponent=1023, mantissa=0), "1.0 must decode to sign=0 exp=1023 mant=0"  # => co-03

    print("\n=== 0.1 + 0.2 != 0.3 ===")  # => co-03: section 4 -- the structural rounding-error demonstration
    total, equals_point_three = demonstrate_rounding_error()  # => co-03: the actual computed sum and its comparison
    print(f"0.1 + 0.2 = {total!r}")  # => co-03: prints the EXACT stored value, not a rounded display
    print(f"0.1 + 0.2 == 0.3: {equals_point_three}")  # => co-03: the headline claim -- expect False
    assert repr(total) == "0.30000000000000004", "must print the syllabus's documented exact value"  # => co-03
    assert equals_point_three is False, "0.1 + 0.2 must NOT equal the literal 0.3"  # => co-03: the structural fact

    print("\nAll representation and IEEE-754 claims verified: True")  # => co-01, co-02, co-03: every assert above passed
    # => co-01: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
    # => co-01, co-02, co-03: this module packages Examples 1, 3, and 6's standalone demonstrations as importable, reusable functions
    # => co-03: Ieee754Fields is a NamedTuple so its three fields (sign/exponent/mantissa) compare by VALUE, enabling the exact-match assert below
    # => co-02: to_twos_complement's bitmask-and-format approach generalizes Example 3's fixed 8-bit case to any bit width
    # => co-01: int_to_binary and int_to_hex share the same shape -- both delegate to Python's own builtin, then strip its base-specific prefix
