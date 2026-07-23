# learning/code/ex-26-alu-op-model/alu_op_model.py
"""Example 26: A Register File Feeding an ALU Operation."""  # => co-15: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from typing import NamedTuple  # => co-15: typed results beat bare tuples for the flag/result pair


class AluResult(NamedTuple):  # => co-15: what a real ALU exposes -- a result AND status flags
    result: int  # => co-15: the 8-bit wrapped arithmetic result
    zero_flag: bool  # => co-15: set when result == 0 -- a real CPU flag, used by conditional branches
    carry_flag: bool  # => co-15: set when the UNWRAPPED sum overflowed the 8-bit word width


class RegisterFile:  # => co-15: a small bank of named registers, feeding operands into the ALU
    """A tiny register file: named 8-bit registers an ALU op reads from."""  # => co-15: documents RegisterFile's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-15: two general-purpose registers, both start at 0
        self.registers: dict[str, int] = {"R0": 0, "R1": 0}  # => co-15: named, addressable fast storage

    def set(self, name: str, value: int) -> None:  # => co-15: writes a value into a named register
        self.registers[name] = value & 0xFF  # => co-15: registers are 8-bit wide -- values are masked on write


def alu_add(a: int, b: int) -> AluResult:  # => co-15: the ALU's add operation -- pure function of its two inputs
    """ALU add: computes an 8-bit sum and derives the zero/carry status flags."""  # => co-15: documents alu_add's contract -- no runtime output, just sets its __doc__
    raw_sum = a + b  # => co-15: the UNWRAPPED sum -- may exceed 8 bits, which is exactly what carry_flag reports
    wrapped = raw_sum & 0xFF  # => co-15: the 8-bit result an 8-bit register can actually hold
    return AluResult(result=wrapped, zero_flag=(wrapped == 0), carry_flag=(raw_sum > 0xFF))  # => co-15: both flags


if __name__ == "__main__":  # => co-15: entry point -- this block runs only when the file executes directly, not on import
    regs = RegisterFile()  # => co-15: a fresh register file feeding this example's ALU operation
    regs.set("R0", 200)  # => co-15: R0 := 200 -- chosen so R0+R1 overflows an 8-bit register
    regs.set("R1", 100)  # => co-15: R1 := 100 -- 200 + 100 = 300, which does NOT fit in 8 bits (max 255)
    result = alu_add(regs.registers["R0"], regs.registers["R1"])  # => co-15: the register file FEEDS the ALU
    print(f"R0={regs.registers['R0']} R1={regs.registers['R1']}")  # => co-15: the two operands read from registers
    print(f"result={result.result} zero_flag={result.zero_flag} carry_flag={result.carry_flag}")  # => co-15
    assert result.result == (300 & 0xFF), "wrapped result must be 300 mod 256 = 44"  # => co-15: 300 - 256 = 44
    assert result.carry_flag is True, "300 exceeds 8 bits -- carry_flag must be set"  # => co-15: overflow detected
    assert result.zero_flag is False, "44 is not zero -- zero_flag must be clear"  # => co-15: correctly NOT zero
    print(f"Flag/result pair matches the expected 8-bit overflow: True")  # => co-15: all three asserts passed
    # => co-15: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
