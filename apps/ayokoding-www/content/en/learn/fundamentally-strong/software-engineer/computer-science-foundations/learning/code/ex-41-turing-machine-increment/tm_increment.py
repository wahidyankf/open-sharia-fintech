# learning/code/ex-41-turing-machine-increment/tm_increment.py
"""Example 41: A Turing Machine Incrementing a Binary Number on Its Tape."""  # => co-22: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

BLANK = "_"  # => co-22: the tape is INFINITE in both directions -- unvisited cells read as this blank symbol
# ex-41: δ -- (state, read symbol) -> (new state, write symbol, move direction). This machine
# implements binary increment: scan to the rightmost digit, then ripple a carry leftward.
TRANSITIONS: dict[tuple[str, str], tuple[str, str, str]] = {  # => co-22: the Turing machine's full transition function
    ("scan_right", "0"): ("scan_right", "0", "R"),  # => co-22: keep moving right over existing digits, unchanged
    ("scan_right", "1"): ("scan_right", "1", "R"),  # => co-22: keep moving right over existing digits, unchanged
    ("scan_right", BLANK): ("increment", BLANK, "L"),  # => co-22: past the last digit -- turn around, start carrying
    ("increment", "0"): ("done", "1", "R"),  # => co-22: 0+1=1, NO further carry -- this is where the machine halts
    ("increment", "1"): ("increment", "0", "L"),  # => co-22: 1+1=10 -- write 0, carry the 1 one cell further left
    ("increment", BLANK): ("done", "1", "R"),  # => co-22: carried past the leftmost digit -- grow the number by one digit
}  # => co-22: closes the multi-line construct opened above
HALT_STATES = {"done"}  # => co-22: no outgoing transitions are defined FROM these states -- the machine stops here


def run_tm(tape_input: str) -> str:  # => co-22: read/write/move state machine over the (conceptually infinite) tape
    """Run the binary-increment Turing machine on tape_input; return the final tape content, trimmed of blanks."""  # => co-22: documents run_tm's contract -- no runtime output, just sets its __doc__
    tape: dict[int, str] = {i: c for i, c in enumerate(tape_input)}  # => co-22: sparse tape -- only written cells exist
    head = 0  # => co-22: the read/write head's current cell position
    state = "scan_right"  # => co-22: the machine's initial state
    steps = 0  # => co-22: a hard cap, purely to guarantee this demo terminates even if a transition table were buggy
    while state not in HALT_STATES and steps < 1000:  # => co-22: run until a halt state OR the safety cap
        symbol = tape.get(head, BLANK)  # => co-22: READ -- an unvisited cell reads as blank, by definition
        new_state, write_symbol, direction = TRANSITIONS[(state, symbol)]  # => co-22: δ -- the ONE next action
        tape[head] = write_symbol  # => co-22: WRITE -- overwrite the current cell
        head += 1 if direction == "R" else -1  # => co-22: MOVE -- exactly one cell, left or right
        state = new_state  # => co-22: transition to the next state
        steps += 1  # => co-22: counts actual machine steps, for the safety cap above
    lo, hi = min(tape), max(tape)  # => co-22: the tape's used extent, for rendering the final result as a string
    return "".join(tape.get(i, BLANK) for i in range(lo, hi + 1)).strip(BLANK)  # => co-22: trim unused blank cells


if __name__ == "__main__":  # => co-22: entry point -- this block runs only when the file executes directly, not on import
    binary_11 = "1011"  # => co-22: 11 in binary -- incrementing should produce 12 ("1100")
    result = run_tm(binary_11)  # => co-22: runs the increment machine end to end
    print(f"tape before: {binary_11} (decimal {int(binary_11, 2)})")  # => co-22: shows the input and its decimal value
    print(f"tape after:  {result} (decimal {int(result, 2)})")  # => co-22: shows the final tape and its decimal value
    assert result == "1100", "incrementing 1011 (11) must produce 1100 (12)"  # => co-22: exact final-tape check
    assert int(result, 2) == int(binary_11, 2) + 1, "the decimal value must have increased by exactly 1"  # => co-22
    print(f"Final tape matches 11 + 1 = 12 in binary: True")  # => co-22: reached only if both asserts passed
    # => co-22: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
