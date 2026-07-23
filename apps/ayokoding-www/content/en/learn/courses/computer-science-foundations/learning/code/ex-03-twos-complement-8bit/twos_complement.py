# learning/code/ex-03-twos-complement-8bit/twos_complement.py
"""Example 3: -42 in 8-Bit Two's Complement."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

BITS = 8  # => co-02: the fixed word width this whole example works in


def to_twos_complement(n: int, bits: int = BITS) -> str:  # => co-02: negative -> 8-bit two's-complement bits
    """Render a signed int in `bits`-wide two's complement, as a bit string."""  # => co-02: documents to_twos_complement's contract -- no runtime output, just sets its __doc__
    mask = (1 << bits) - 1  # => co-02: 0xFF for bits=8 -- keeps only the low `bits` bits
    encoded = n & mask  # => co-02: Python ints are arbitrary-precision, so AND-with-mask IS the
    # => two's-complement encoding -- invert-and-add-1 is what `&` with a negative int does internally
    return format(encoded, f"0{bits}b")  # => co-02: zero-padded binary string, e.g. "11010110"


if __name__ == "__main__":  # => co-02: entry point -- this block runs only when the file executes directly, not on import
    value = -42  # => co-02: the syllabus's fixed test value
    bits = to_twos_complement(value)  # => co-02: the 8-bit two's-complement pattern
    print(f"to_twos_complement({value}) = {bits}")  # => co-02: prints the bit pattern
    assert bits == "11010110", "must match the syllabus's documented pattern"  # => co-02: exact-match check
    identity = (value & 0xFF) + 42  # => co-02: the defining property -- complement + magnitude == 2**bits
    print(f"(-42 & 0xFF) + 42 = {identity}")  # => co-02: prints the identity check
    assert identity == 256, "two's-complement identity must hold: complement + |n| == 2**bits"  # => co-02
    print(f"Pattern matches, identity holds: True")  # => co-02: reached only if both asserts passed
    # => co-02: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
