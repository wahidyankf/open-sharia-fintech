# learning/code/ex-01-dec-to-binary-by-division/dec_to_binary.py
"""Example 1: Decimal to Binary by Repeated Division."""  # => co-01: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic
# => __future__ import: DD-39 hygiene so `list[int]` below reads identically on
# => every supported interpreter, unrelated to the conversion algorithm itself


def to_binary(n: int) -> str:  # => co-01: positional-system conversion via repeated division
    """Convert a non-negative int to its binary string by repeated division by 2."""  # => co-01: documents to_binary's contract -- no runtime output, just sets its __doc__
    if n == 0:  # => co-01: the one base case repeated division never reaches on its own
        return "0"  # => co-01: 0 in any base is just "0" -- short-circuit before the loop
    remainders: list[int] = []  # => co-01: collects bits LEAST-significant-first, one per division
    working = n  # => co-01: a local copy -- the loop mutates this, never the caller's `n`
    while working > 0:  # => co-01: stop the instant the quotient reaches 0
        remainders.append(working % 2)  # => co-01: the next bit is this step's remainder (0 or 1)
        working //= 2  # => co-01: integer-divide by the base (2) -- the "repeated division" step
    return "".join(str(bit) for bit in reversed(remainders))  # => co-01: reverse -- bits came out LSB-first


if __name__ == "__main__":  # => co-01: entry point -- this block runs only when the file executes directly, not on import
    n = 156  # => co-01: the syllabus's fixed test value
    result = to_binary(n)  # => co-01: hand-rolled positional-division conversion
    expected = bin(n)[2:]  # => co-01: Python's own built-in conversion, stripped of its "0b" prefix
    print(f"to_binary({n}) = {result}")  # => co-01: prints the hand-rolled result
    print(f"bin({n})       = 0b{expected}")  # => co-01: prints Python's own conversion for comparison
    assert result == expected, "hand-rolled conversion must match bin()"  # => co-01: the two must agree
    print(f"MATCH: {result == expected}")  # => co-01: confirms agreement -- expect "10011100"
    # => co-01: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
