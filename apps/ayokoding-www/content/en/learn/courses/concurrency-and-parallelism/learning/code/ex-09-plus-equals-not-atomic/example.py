"""Example 9: `x += 1` Is Not One Atomic Step -- Proof via `dis`."""

import dis  # => the stdlib bytecode disassembler -- makes co-10's claim inspectable, not just asserted
import types  # => types.FunctionType -- the precise type `dis.get_instructions` accepts


def bump() -> None:  # => a tiny function whose ONLY job is to be disassembled
    global shared  # => refers to the module-level `shared` global below
    shared = shared + 1  # => the exact statement whose atomicity (or lack of it) this example proves


shared = 0  # => the global `bump()` mutates -- irrelevant to the bytecode shape itself


def opnames_for(func: types.FunctionType) -> list[str]:  # => extracts opcode NAMES, in execution order
    return [instr.opname for instr in dis.get_instructions(func)]  # => one name per bytecode instruction


if __name__ == "__main__":  # => module entry point
    names = opnames_for(bump)  # => names: the full list of opcodes CPython compiled `bump` into
    print(names)  # => Output: ['RESUME', 'LOAD_GLOBAL', 'LOAD_SMALL_INT', 'BINARY_OP', 'STORE_GLOBAL', ...]

    # => `shared = shared + 1` compiles to (at least) three SEPARATE steps: read the current value
    # => (LOAD_GLOBAL), compute the new one (BINARY_OP), then write it back (STORE_GLOBAL). Any of
    # => CPython's bytecode-boundary thread switches (co-08) can land BETWEEN these three steps.
    assert "LOAD_GLOBAL" in names  # => step 1: read the current value of `shared`
    assert "BINARY_OP" in names  # => step 2: compute `shared + 1` -- NOT yet written anywhere
    assert "STORE_GLOBAL" in names  # => step 3: write the new value back to `shared`
    load_idx = names.index("LOAD_GLOBAL")  # => load_idx: the position of the read
    store_idx = names.index("STORE_GLOBAL")  # => store_idx: the position of the write
    assert load_idx < store_idx  # => confirms the read happens strictly BEFORE the write, not fused
    print("ex-09 OK")  # => Output: ex-09 OK
