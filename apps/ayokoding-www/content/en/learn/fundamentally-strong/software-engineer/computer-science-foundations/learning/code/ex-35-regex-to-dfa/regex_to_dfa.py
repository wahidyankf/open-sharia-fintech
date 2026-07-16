# learning/code/ex-35-regex-to-dfa/regex_to_dfa.py
"""Example 35: Mapping the Regex (ab)* to an Accepting DFA."""  # => co-19: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import re  # => co-19: Python's own regex engine -- the "regex" half of Kleene's regex/FA equivalence

REGEX = re.compile(r"^(ab)*$")  # => co-19: matches zero or more repetitions of exactly "ab", anchored both ends

# ex-35: a hand-built DFA for the SAME language {(ab)^n : n >= 0} -- Kleene's theorem says a
# regex and a DFA for the same language must classify every string IDENTICALLY.
DFA_TRANSITIONS: dict[tuple[str, str], str] = {  # => co-19: δ for the hand-built (ab)* DFA
    ("S", "a"): "MID",  # => co-19: S (accepting -- "even count so far") sees "a" -> mid-pair state
    ("MID", "b"): "S",  # => co-19: MID sees "b" -> completes a pair, back to accepting S
    ("S", "b"): "DEAD",  # => co-19: S seeing "b" first is never valid in (ab)* -- trap state
    ("MID", "a"): "DEAD",  # => co-19: MID seeing "a" again (two a's in a row) is never valid -- trap state
    ("DEAD", "a"): "DEAD",
    ("DEAD", "b"): "DEAD",  # => co-19: DEAD is a sink -- no escape once trapped
}  # => co-19: closes the multi-line construct opened above
DFA_ACCEPT = {"S"}  # => co-19: only S accepts -- exactly "an even, complete number of ab pairs so far"


def run_dfa(s: str) -> bool:  # => co-19: the hand-built machine's own accept/reject verdict
    """Run the hand-built (ab)* DFA on s."""  # => co-19: documents run_dfa's contract -- no runtime output, just sets its __doc__
    state = "S"  # => co-19: start state -- zero pairs consumed is itself accepting (n=0 case)
    for symbol in s:  # => co-19: one transition per character
        state = DFA_TRANSITIONS.get((state, symbol), "DEAD")  # => co-19: any undefined symbol also traps
    return state in DFA_ACCEPT  # => co-19: accepted iff the walk ends back in S


if __name__ == "__main__":  # => co-19: entry point -- this block runs only when the file executes directly, not on import
    test_cases = ["", "ab", "abab", "ababab", "a", "aba", "ba", "abba", "aabb"]  # => co-19: a spread of strings
    for s in test_cases:  # => co-19: run EVERY string through both the regex and the hand-built DFA
        regex_verdict = REGEX.fullmatch(s) is not None  # => co-19: the regex engine's own verdict
        dfa_verdict = run_dfa(s)  # => co-19: the hand-built DFA's verdict for the SAME string
        print(f"{s!r:<8} regex={regex_verdict} dfa={dfa_verdict}")  # => co-19: side-by-side comparison
        assert regex_verdict == dfa_verdict, f"regex and DFA must agree on {s!r} (Kleene's theorem)"  # => co-19
    print(f"Regex and hand-built DFA classify every test string identically: True")  # => co-19: all asserts passed
    # => co-19: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
