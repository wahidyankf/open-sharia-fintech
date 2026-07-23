# learning/code/ex-38-pda-anbn/pda_anbn.py
"""Example 38: A Pushdown Automaton (FA + Stack) Accepting a^n b^n."""  # => co-20: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def run_pda(s: str) -> bool:  # => co-20: a PDA -- exactly an FA plus one stack, and the stack is what a DFA lacks
    """Run a pushdown automaton on s: push a Z marker per 'a', pop one per 'b'; accept iff the stack empties."""  # => co-20: documents run_pda's contract -- no runtime output, just sets its __doc__
    stack: list[str] = []  # => co-20: the ONE piece of unbounded memory a plain FA never has
    i = 0  # => co-20: input head position -- an FA-style left-to-right scan
    while i < len(s) and s[i] == "a":  # => co-20: PHASE 1 -- every leading "a" PUSHES one marker
        stack.append("Z")  # => co-20: the stack now records EXACTLY how many "a"s have been seen so far
        i += 1  # => co-20: advance the input head
    while i < len(s) and s[i] == "b":  # => co-20: PHASE 2 -- every "b" must POP one marker
        if not stack:  # => co-20: a "b" with nothing left to pop means MORE b's than a's -- reject
            return False  # => co-20: stack underflow -- this string is not in a^n b^n
        stack.pop()  # => co-20: one "b" consumes exactly one "a"'s marker -- this IS the n==n check
        i += 1  # => co-20: advance the input head
    consumed_everything = i == len(s)  # => co-20: no leftover input (e.g. a stray extra character) is allowed
    stack_empty = len(stack) == 0  # => co-20: EXACTLY as many b's as a's -- the stack must be back to empty
    return consumed_everything and stack_empty  # => co-20: accept iff BOTH conditions hold


if __name__ == "__main__":  # => co-20: entry point -- this block runs only when the file executes directly, not on import
    test_cases = {  # => co-20: string -> hand-verified a^n b^n membership
        "": True,  # => co-20: n=0 -- the empty string is trivially a^0 b^0
        "ab": True,  # => co-20: n=1 -- one push, one matching pop, stack ends empty
        "aabb": True,  # => co-20: n=2 -- two pushes, two matching pops
        "aaabbb": True,  # => co-20: n=0,1,2,3 -- all valid a^n b^n
        "a": False,  # => co-20: pushes but never pops -- stack non-empty at the end
        "b": False,  # => co-20: pops with nothing pushed -- immediate stack underflow
        "aab": False,  # => co-20: two pushes, only one pop -- stack non-empty at the end
        "abb": False,  # => co-20: one push, second "b" hits an empty stack -- underflow
        "ba": False,  # => co-20: unequal counts or wrong order
    }  # => co-20: closes the multi-line construct opened above
    for s, expected in test_cases.items():  # => co-20: run every case through the PDA simulator
        actual = run_pda(s)  # => co-20: the PDA's own accept/reject verdict
        print(f"{s!r:<7} accepted={actual} expected={expected}")  # => co-20: per-case report
        assert actual == expected, f"PDA verdict for {s!r} must be {expected}"  # => co-20
    print(f"All a^n b^n strings correctly accepted, all others rejected: True")  # => co-20: every assert passed
    # => co-20: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
