# learning/code/ex-14-half-adder/half_adder.py
"""Example 14: The Half-Adder -- sum = XOR, carry = AND."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-07: enumerates every input pair -- the half-adder's full truth table
from typing import NamedTuple  # => co-07: typing import supporting the typed structures below


class HalfAdderResult(NamedTuple):  # => co-07: a half-adder's two outputs -- the sum bit and the carry-out bit
    sum_bit: bool  # => co-08: this bit's own result, ignoring any carry INTO this position
    carry_bit: bool  # => co-08: overflow into the NEXT-more-significant bit position


def half_adder(a: bool, b: bool) -> HalfAdderResult:  # => co-08: a COMBINATIONAL circuit -- pure function of a, b
    """Add two single bits: sum via XOR, carry-out via AND."""  # => co-08: documents half_adder's contract -- no runtime output, just sets its __doc__
    sum_bit = a != b  # => co-07: XOR -- 1+0 or 0+1 give sum=1; 0+0 or 1+1 give sum=0 (the 1+1 case carries)
    carry_bit = a and b  # => co-07: AND -- carry fires ONLY when both bits are 1 (1+1=10 in binary)
    return HalfAdderResult(sum_bit, carry_bit)  # => co-07: returns this computed value to the caller


if __name__ == "__main__":  # => co-07: entry point -- this block runs only when the file executes directly, not on import
    expected = {  # => co-07: the half-adder's textbook truth table, to check the circuit against
        (False, False): (False, False),  # => 0+0 = 0, no carry
        (False, True): (True, False),  # => 0+1 = 1, no carry
        (True, False): (True, False),  # => 1+0 = 1, no carry
        (True, True): (False, True),  # => 1+1 = 10 in binary -- sum bit 0, carry bit 1
    }  # => co-07: closes the multi-line construct opened above
    for a, b in itertools.product([False, True], repeat=2):  # => co-08: all 4 input combinations
        result = half_adder(a, b)  # => co-08: run the combinational circuit for this input pair
        want_sum, want_carry = expected[(a, b)]  # => co-07: the textbook answer for this exact pair
        print(f"{int(a)} + {int(b)} -> sum={int(result.sum_bit)} carry={int(result.carry_bit)}")  # => co-07
        assert result.sum_bit == want_sum, f"sum bit mismatch for {a}, {b}"  # => co-07: matches truth table
        assert result.carry_bit == want_carry, f"carry bit mismatch for {a}, {b}"  # => co-07: matches truth table
    print("Half-adder matches its textbook truth table on all 4 rows: True")  # => co-08: full proof complete
    # => co-08: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
