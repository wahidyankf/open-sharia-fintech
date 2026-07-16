# learning/capstone/code/automaton.py
"""Capstone Step 2: a finite-automaton simulator, run against a hand-traced regular language.

Ties together co-18 (finite automata) and co-19 (regex-to-FA equivalence, Kleene's theorem) into
one reusable Dfa class -- the same shape Example 33's generic simulator introduced -- instantiated
here for a NEW language: binary strings ENDING in the substring "01".
"""  # => co-18: this file's own restated purpose, doubling as its module __doc__
# => co-18: no runtime output beyond setting __doc__ -- the three paragraphs above just orient the reader

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import re  # => co-19: Python's own regex engine -- the independent cross-check for Kleene's theorem
from dataclasses import dataclass  # => co-19: stdlib-only import backing this example

# ex-capstone: L = { w in {0,1}* : w ends with "01" }. Hand-traced transition table below --
# state Si tracks "have we just seen the prefix of '01' needed to accept if the string ended here":
#   S0 = "last symbol read was NOT a 0 that could start '01'" (or nothing read yet)
#   S1 = "last symbol read was a 0" (a potential start of '01')
#   S2 = "last two symbols read were exactly '0' then '1'" (ACCEPTING -- ends in "01" right now)
TRANSITIONS: dict[tuple[str, str], str] = {  # => co-18: δ -- the full transition table for this DFA
    ("S0", "0"): "S1",  # => co-18: from S0, a "0" moves toward acceptance (potential start of "01")
    ("S0", "1"): "S0",  # => co-18: from S0, a "1" stays put -- can't start "01" with a "1"
    ("S1", "0"): "S1",  # => co-18: from S1, another "0" stays (still "just saw a 0")
    ("S1", "1"): "S2",  # => co-18: from S1, "1" completes "01" -- move to the accepting state
    ("S2", "0"): "S1",  # => co-18: from S2, a NEW "0" restarts the watch for another "01"
    ("S2", "1"): "S0",  # => co-18: from S2, "1" breaks the ending -- back to "not watching"
}  # => co-18: closes the multi-line construct opened above
ACCEPT = {"S2"}  # => co-18: F -- accepting iff the walk currently ends in S2 ("...01" just seen)
REGEX = re.compile(r".*01$")  # => co-19: the SAME language, expressed as a regex -- Kleene's theorem says these must agree


@dataclass(frozen=True)  # => co-18: a DFA is DATA -- reusable for any (states, alphabet, δ, start, accept) tuple
class Dfa:  # => co-18: continues the statement started above
    transitions: dict[tuple[str, str], str]  # => co-18: δ
    start: str  # => co-18: q0
    accept: set[str]  # => co-18: F

    def run(self, s: str) -> bool:  # => co-18: feed s through δ symbol by symbol, from q0
        state = self.start  # => co-18: every run begins at q0, unconditionally
        for symbol in s:  # => co-18: one transition per symbol -- exactly one next state each step
            state = self.transitions[(state, symbol)]  # => co-18: δ(state, symbol)
        return state in self.accept  # => co-18: accepted iff the FINAL state is in F


ENDS_IN_01 = Dfa(transitions=TRANSITIONS, start="S0", accept=ACCEPT)  # => co-18: the machine this step exercises


if __name__ == "__main__":  # => co-18: entry point -- this block runs only when the file executes directly, not on import
    # Hand trace for "001": S0 -0-> S1 -0-> S1 -1-> S2. Final state S2 is accepting, so "001" IS
    # accepted -- and indeed "001" genuinely ends with the substring "01".
    test_cases = ["", "0", "1", "01", "10", "001", "110", "0101", "0110", "111101"]  # => co-18: a spread of strings
    for s in test_cases:  # => co-18, co-19: run every string through BOTH the DFA and the regex
        dfa_verdict = ENDS_IN_01.run(s)  # => co-18: the hand-built machine's own accept/reject verdict
        regex_verdict = REGEX.fullmatch(s) is not None  # => co-19: Kleene's theorem's independent cross-check
        ends_with_01 = s.endswith("01")  # => co-18: a THIRD, brute-force sanity check against plain string logic
        print(f"{s!r:<8} dfa={dfa_verdict} regex={regex_verdict} ends_with_01={ends_with_01}")  # => co-18, co-19
        assert dfa_verdict == regex_verdict == ends_with_01, f"all three checks must agree for {s!r}"  # => co-18, co-19
    print("\nHand trace for '001': S0 -0-> S1 -0-> S1 -1-> S2 (accepting)")  # => co-18: documents the trace by hand
    assert ENDS_IN_01.run("001") is True, "the hand-traced walk for '001' must land in the accepting state S2"  # => co-18
    print("Every test string classified correctly against its hand-traced expectation: True")  # => co-18, co-19
    # => co-18: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
    # => co-18: Dfa is declared frozen -- once built, a DFA's transition table never mutates mid-run, matching the formal (Q, Sigma, delta, q0, F) definition
    # => co-19: REGEX and TRANSITIONS encode the identical language two different ways -- Kleene's theorem guarantees they must agree on every input
    # => co-18: the hand-traced walk for "001" in the comment above is exactly what Dfa.run replays mechanically, symbol by symbol
