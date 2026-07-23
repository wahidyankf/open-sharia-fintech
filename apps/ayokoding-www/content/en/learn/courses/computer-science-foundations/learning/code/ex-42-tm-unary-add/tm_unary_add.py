# learning/code/ex-42-tm-unary-add/tm_unary_add.py
"""Example 42: A Turing Machine Adding Two Unary Numbers."""  # => co-22: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

BLANK = "_"  # => co-22: unvisited cells read as blank -- the tape is conceptually unbounded in both directions
# ex-42: input format is "1"*m + "+" + "1"*n (m and n in UNARY). Algorithm: replace the "+" with
# a "1" (now m+n+1 ones total), scan to the end, then erase exactly one trailing "1" -- leaving m+n.
TRANSITIONS: dict[tuple[str, str], tuple[str, str, str]] = {  # => co-22: δ for this unary-addition machine
    ("seek_plus", "1"): ("seek_plus", "1", "R"),  # => co-22: skip over the m leading 1s, unchanged
    ("seek_plus", "+"): ("seek_end", "1", "R"),  # => co-22: the "+" becomes a "1" -- this is the merge step
    ("seek_end", "1"): ("seek_end", "1", "R"),  # => co-22: skip over the n trailing 1s, unchanged
    ("seek_end", BLANK): ("erase_one", BLANK, "L"),  # => co-22: past the last 1 -- step back onto it
    ("erase_one", "1"): ("done", BLANK, "R"),  # => co-22: erase exactly ONE 1 -- corrects the +1 from the merge step
}  # => co-22: closes the multi-line construct opened above
HALT_STATES = {"done"}  # => co-22: no outgoing transitions defined from "done" -- the machine stops here


def run_tm(tape_input: str) -> str:  # => co-22: read/write/move state machine, same mechanism as Example 41
    """Run the unary-addition Turing machine; return the final tape, trimmed of blank cells."""  # => co-22: documents run_tm's contract -- no runtime output, just sets its __doc__
    tape: dict[int, str] = {i: c for i, c in enumerate(tape_input)}  # => co-22: sparse tape representation
    head = 0  # => co-22: read/write head position
    state = "seek_plus"  # => co-22: initial state -- scanning past the first operand's 1s
    steps = 0  # => co-22: safety cap, unrelated to the algorithm itself
    while state not in HALT_STATES and steps < 1000:  # => co-22: run until halted or the safety cap trips
        symbol = tape.get(head, BLANK)  # => co-22: READ
        new_state, write_symbol, direction = TRANSITIONS[(state, symbol)]  # => co-22: δ -- the one next action
        tape[head] = write_symbol  # => co-22: WRITE
        head += 1 if direction == "R" else -1  # => co-22: MOVE, exactly one cell
        state = new_state  # => co-22: transition
        steps += 1  # => co-22: step counter for the safety cap
    lo, hi = min(tape), max(tape)  # => co-22: used tape extent
    return "".join(tape.get(i, BLANK) for i in range(lo, hi + 1)).strip(BLANK)  # => co-22: trimmed final tape


if __name__ == "__main__":  # => co-22: entry point -- this block runs only when the file executes directly, not on import
    m, n = 3, 2  # => co-22: computing 3 + 2 in unary -- expect 5 ones on the final tape
    tape_input = ("1" * m) + "+" + ("1" * n)  # => co-22: "111+11" -- the machine's starting tape
    result = run_tm(tape_input)  # => co-22: runs the unary-addition machine end to end
    print(f"tape before: {tape_input!r}  ({m} + {n})")  # => co-22: shows the input and the sum it represents
    print(f"tape after:  {result!r}  ({len(result)} ones)")  # => co-22: shows the final tape and its 1-count
    assert result == "1" * (m + n), "the final tape must be exactly m+n ones, no '+' and no stray blanks"  # => co-22
    assert len(result) == 5, "3 + 2 in unary must produce exactly 5 ones"  # => co-22: the syllabus's exact claim
    print(f"Tape result equals the sum {m} + {n} = {len(result)}: True")  # => co-22: both asserts above passed
    # => co-22: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
