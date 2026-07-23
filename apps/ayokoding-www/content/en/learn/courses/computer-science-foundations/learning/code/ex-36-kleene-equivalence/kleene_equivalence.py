# learning/code/ex-36-kleene-equivalence/kleene_equivalence.py
"""Example 36: Kleene Equivalence -- re.match vs. a Hand-Built DFA, Exhaustive Agreement."""  # => co-19: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-19: generates EVERY string up to a bound, an exhaustive (not sampled) agreement check
import re  # => co-19: Python's regex engine -- one of the two independent implementations being compared

REGEX = re.compile(r"^a+b+$")  # => co-19: one or more "a"s, then one or more "b"s -- language L = {a^i b^j : i,j >= 1}

DFA_TRANSITIONS: dict[tuple[str, str], str] = {  # => co-19: δ for a hand-built DFA of the SAME language
    ("Q0", "a"): "Q1",  # => co-19: Q0 (start, non-accepting) -- first "a" moves to "seen at least one a"
    ("Q1", "a"): "Q1",  # => co-19: Q1 -- more "a"s keep us in Q1 (still "in the a-run")
    ("Q1", "b"): "Q2",  # => co-19: Q1 -- first "b" moves to "seen at least one b after the a-run"
    ("Q2", "b"): "Q2",  # => co-19: Q2 (accepting) -- more "b"s keep us in Q2
}  # => co-19: closes the multi-line construct opened above
DFA_ACCEPT = {"Q2"}  # => co-19: only Q2 accepts -- at least one a, THEN at least one b, nothing else


def run_dfa(s: str) -> bool:  # => co-19: the hand-built machine's own accept/reject verdict, DEAD on any gap
    """Run the hand-built a+b+ DFA on s."""  # => co-19: documents run_dfa's contract -- no runtime output, just sets its __doc__
    state = "Q0"  # => co-19: start state
    for symbol in s:  # => co-19: any undefined (state, symbol) pair traps into rejection via .get()'s default
        state = DFA_TRANSITIONS.get((state, symbol), "DEAD")  # => co-19: DEAD has no outgoing transitions defined
    return state in DFA_ACCEPT  # => co-19: accepted iff the walk ends in Q2


if __name__ == "__main__":  # => co-19: entry point -- this block runs only when the file executes directly, not on import
    alphabet = ("a", "b")  # => co-19: the two symbols this language's alphabet is built from
    all_strings: list[str] = [""]  # => co-19: length 0 first
    for length in range(1, 6):  # => co-19: EVERY string of length 1 through 5 over {a, b} -- 2+4+...+32 = 62 strings
        all_strings.extend("".join(combo) for combo in itertools.product(alphabet, repeat=length))  # => co-19
    mismatches: list[str] = []  # => co-19: any string where the two implementations disagree
    for s in all_strings:  # => co-19: exhaustive comparison, not a hand-picked sample
        regex_verdict = REGEX.fullmatch(s) is not None  # => co-19: Python's own regex engine's verdict
        dfa_verdict = run_dfa(s)  # => co-19: the hand-built DFA's verdict for the same string
        if regex_verdict != dfa_verdict:  # => co-19: record any disagreement for the final report
            mismatches.append(s)  # => co-19: expected to stay empty across all 63 strings
    print(f"checked {len(all_strings)} strings up to length 5, mismatches: {mismatches}")  # => co-19
    assert mismatches == [], "regex and hand-built DFA must agree on every string checked"  # => co-19
    assert run_dfa("ab") and run_dfa("aaabbb") and not run_dfa("ba") and not run_dfa("")  # => co-19: spot checks
    print(f"Regex and DFA agree on all {len(all_strings)} inputs: True")  # => co-19: the exhaustive check passed
    # => co-19: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
