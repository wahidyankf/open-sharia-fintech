# learning/code/ex-04-subtraction-as-addition/subtraction_as_addition.py
"""Example 4: Subtraction as Addition -- 5 - 3 via Two's-Complement Add."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

BITS = 8  # => co-02: one fixed adder width for both operands


def negate_8bit(n: int) -> int:  # => co-02: two's-complement negation -- invert bits, add 1, mask to 8 bits
    """Return the 8-bit two's-complement encoding of -n, as an unsigned int 0..255."""  # => co-02: documents negate_8bit's contract -- no runtime output, just sets its __doc__
    return ((~n) + 1) & 0xFF  # => co-02: `~n` inverts every bit, `+1` completes two's complement, mask keeps 8 bits


def add_8bit(a: int, b: int) -> int:  # => co-02: the SAME adder used for a - b below, unmodified
    """Add two 8-bit unsigned patterns, discarding any carry past bit 7 (wraparound)."""  # => co-02: documents add_8bit's contract -- no runtime output, just sets its __doc__
    return (a + b) & 0xFF  # => co-02: masking after the add is exactly what an 8-bit ALU's carry-out does


if __name__ == "__main__":  # => co-02: entry point -- this block runs only when the file executes directly, not on import
    a, b = 5, 3  # => co-02: the syllabus's fixed operands -- computing a - b as a + (-b)
    neg_b = negate_8bit(b)  # => co-02: -3 encoded as an 8-bit two's-complement PATTERN, not a Python int
    print(f"a = {a} = {a:08b}")  # => co-02: operand a in binary, for the reader to follow along
    print(f"-b = -{b} encoded as {neg_b:08b} (two's complement of {b})")  # => co-02: the negated operand's bits
    low_byte = add_8bit(a, neg_b)  # => co-02: ONE addition circuit computes 5 + (-3) -- no separate "subtract" op
    print(f"a + (-b) low byte = {low_byte:08b} = {low_byte}")  # => co-02: the adder's 8-bit result
    assert low_byte == 2, "5 - 3 must equal 2 via two's-complement addition"  # => co-02: matches ordinary subtraction
    print(f"Matches ordinary 5 - 3 = {a - b}: True")  # => co-02: the same adder never needed a subtract circuit
    # => co-02: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
