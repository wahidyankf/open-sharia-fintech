# learning/code/ex-44-busy-beaver-intuition/busy_beaver.py
"""Example 44: A Small Turing Machine Whose Halting Is Hard to Predict -- Only Running It Tells You."""  # => co-23: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

BLANK = "0"  # => co-23: this machine's blank symbol -- the tape starts entirely "0"
HALT = "HALT"  # => co-23: a plain state name, not None -- transitioning here IS this machine's only halt action
# ex-44: the known 2-state, 2-symbol "busy beaver" champion (BB(2)) -- the machine that runs
# LONGEST among all 2-state/2-symbol machines that eventually halt. No formula predicts this in
# general (that IS the halting problem, co-23) -- the only way to know is to simulate it and see.
TRANSITIONS: dict[tuple[str, str], tuple[str, str, str]] = {  # => co-23: δ -- every (state, symbol) pair is defined
    ("A", "0"): ("B", "1", "R"),  # => co-23: state A reading 0: write 1, move right, go to B
    ("A", "1"): ("B", "1", "L"),  # => co-23: state A reading 1: write 1, move left, go to B
    ("B", "0"): ("A", "1", "L"),  # => co-23: state B reading 0: write 1, move left, go to A
    ("B", "1"): (HALT, "1", "R"),  # => co-23: state B reading 1: write 1, move right, transition to HALT
}  # => co-23: closes the multi-line construct opened above


def run_busy_beaver(max_steps: int = 1000) -> tuple[bool, int, int]:  # => co-23: (halted, steps_taken, ones_on_tape)
    """Simulate BB(2); return whether it halted within max_steps, how many steps, and the final 1-count."""  # => co-23: documents run_busy_beaver's contract -- no runtime output, just sets its __doc__
    tape: dict[int, str] = {}  # => co-23: sparse tape, starts entirely blank ("0") by construction
    head = 0  # => co-23: read/write head position
    state = "A"  # => co-23: start state
    steps = 0  # => co-23: actual machine steps executed -- this IS the number the busy-beaver function studies
    while state != HALT and steps < max_steps:  # => co-23: run until the HALT state or the safety cap trips
        symbol = tape.get(head, BLANK)  # => co-23: READ
        new_state, write_symbol, direction = TRANSITIONS[(state, symbol)]  # => co-23: δ -- the ONE next action
        tape[head] = write_symbol  # => co-23: WRITE
        head += 1 if direction == "R" else -1  # => co-23: MOVE
        state = new_state  # => co-23: transition (may itself become HALT on this very step)
        steps += 1  # => co-23: one more executed step, including the step that reaches HALT
    ones = sum(1 for v in tape.values() if v == "1")  # => co-23: the "score" busy-beaver studies -- 1s written
    return state == HALT, steps, ones  # => co-23: halted?, how many steps it took, how many 1s remain


if __name__ == "__main__":  # => co-23: entry point -- this block runs only when the file executes directly, not on import
    halted, steps, ones = run_busy_beaver()  # => co-23: the ONLY way to learn this machine's behavior is to run it
    print(f"halted={halted} after {steps} steps, leaving {ones} ones on the tape")  # => co-23: the observed outcome
    assert halted is True, "BB(2)'s known champion machine must halt"  # => co-23: it does, but only simulation shows it
    assert steps == 6, "BB(2)'s champion halts after exactly 6 steps"  # => co-23: the documented busy-beaver(2) value
    assert ones == 4, "BB(2)'s champion leaves exactly 4 ones on the tape when it halts"  # => co-23: documented value
    print(f"Matches the documented BB(2) champion (6 steps, 4 ones): True")  # => co-23: all asserts above passed
    # => co-23: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
