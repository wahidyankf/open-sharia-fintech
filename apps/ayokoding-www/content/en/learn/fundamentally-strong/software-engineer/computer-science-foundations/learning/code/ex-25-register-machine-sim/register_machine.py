# learning/code/ex-25-register-machine-sim/register_machine.py
"""Example 25: A Tiny LOAD/ADD/STORE Register Machine."""  # => co-15: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from typing import NamedTuple  # => co-15: a typed instruction beats a bare tuple for readability


class Instruction(NamedTuple):  # => co-15: one fetch-decode-execute cycle's worth of work
    op: str  # => co-15: the opcode -- "LOAD", "ADD", or "STORE"
    arg: int  # => co-15: LOAD/ADD read a literal value or memory address; STORE writes to an address


class RegisterMachine:  # => co-15: the fetch-decode-execute cycle, a memory array, and one accumulator register
    """A tiny machine: one accumulator register, a flat memory array, LOAD/ADD/STORE opcodes."""  # => co-15: documents RegisterMachine's contract -- no runtime output, just sets its __doc__

    def __init__(self, memory_size: int = 8) -> None:  # => co-15: fixed-size memory, all zero-initialized
        self.accumulator = 0  # => co-15: the ONE fast register this machine has -- all arithmetic goes through it
        self.memory: list[int] = [0] * memory_size  # => co-15: RAM -- addressable by a plain integer index

    def execute(self, program: list[Instruction]) -> int:  # => co-15: runs every instruction, in order, FETCH-DECODE-EXECUTE
        """Run a program of LOAD/ADD/STORE instructions; return the final accumulator value."""  # => co-15: documents execute's contract -- no runtime output, just sets its __doc__
        for instr in program:  # => co-15: FETCH -- pull the next instruction off the program list
            if instr.op == "LOAD":  # => co-15: DECODE -- dispatch on the opcode
                self.accumulator = instr.arg  # => co-15: EXECUTE -- literal load into the accumulator register
            elif instr.op == "ADD":  # => co-15: DECODE -- the ALU's addition operation
                self.accumulator += instr.arg  # => co-15: EXECUTE -- accumulator += literal, via the ALU
            elif instr.op == "STORE":  # => co-15: DECODE -- write the register back out to memory
                self.memory[instr.arg] = self.accumulator  # => co-15: EXECUTE -- memory[address] = accumulator
            else:  # => co-15: an unrecognized opcode is a machine fault, not silently ignored
                raise ValueError(f"unknown opcode: {instr.op}")  # => co-15: fails loudly instead of guessing
        return self.accumulator  # => co-15: the accumulator's final value after every instruction has run


if __name__ == "__main__":  # => co-15: entry point -- this block runs only when the file executes directly, not on import
    program = [  # => co-15: LOAD 10, ADD 5, ADD 7, STORE into memory[0] -- expect accumulator == 22
        Instruction("LOAD", 10),  # => co-15: accumulator := 10
        Instruction("ADD", 5),  # => co-15: accumulator := 10 + 5 = 15
        Instruction("ADD", 7),  # => co-15: accumulator := 15 + 7 = 22
        Instruction("STORE", 0),  # => co-15: memory[0] := 22
    ]  # => co-15: closes the multi-line construct opened above
    machine = RegisterMachine()  # => co-15: a fresh machine, accumulator=0, memory all zeros
    final_accumulator = machine.execute(program)  # => co-15: runs the whole program, cycle by cycle
    print(f"final accumulator = {final_accumulator}")  # => co-15: expect 22
    print(f"memory[0] = {machine.memory[0]}")  # => co-15: expect 22 -- the STORE instruction's effect
    assert final_accumulator == 22, "accumulator must hold 10 + 5 + 7 = 22"  # => co-15: the arithmetic result
    assert machine.memory[0] == 22, "STORE must have written the accumulator's value to memory[0]"  # => co-15
    print(f"Accumulator holds expected result: True")  # => co-15: both asserts above passed
    # => co-15: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
