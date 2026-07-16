# learning/code/ex-32-dfa-even-zeros/dfa_even_zeros.py
"""Example 32: A DFA Accepting Strings with an Even Number of 0s."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

EVEN, ODD = "EVEN", "ODD"  # => co-18: the DFA's two states -- "count of 0s seen so far is even/odd"


def run_dfa(binary_string: str) -> bool:  # => co-18: a DFA -- states, alphabet, transition function, start, accept
    """Run the even-number-of-zeros DFA on a binary string; return True iff it's accepted."""  # => co-18: documents run_dfa's contract -- no runtime output, just sets its __doc__
    state = EVEN  # => co-18: START state -- zero 0s seen so far, which IS even (0 is even)
    for symbol in binary_string:  # => co-18: one transition per input symbol, alphabet = {"0", "1"}
        if symbol == "0":  # => co-18: a "0" symbol FLIPS the parity state
            state = ODD if state == EVEN else EVEN  # => co-18: the transition function's only interesting rule
        elif symbol != "1":  # => co-18: a "1" symbol leaves parity unchanged -- no branch needed for it at all
            raise ValueError(f"symbol {symbol!r} not in alphabet {{0, 1}}")  # => co-18: fails loudly, not silently
    return state == EVEN  # => co-18: ACCEPT state is EVEN -- the only state membership this DFA accepts


if __name__ == "__main__":  # => co-18: entry point -- this block runs only when the file executes directly, not on import
    # ex-32: string -> expected accept/reject, hand-counted number of "0" characters:
    # ""=0 zeros(even), "0"=1(odd), "00"=2(even), "010"=2(even), "0100"=3(odd), "111"=0(even)
    test_cases = {"": True, "0": False, "00": True, "010": True, "0100": False, "111": True}  # => co-18
    for s, expected in test_cases.items():  # => co-18: run every test string through the DFA
        actual = run_dfa(s)  # => co-18: the DFA's own accept/reject verdict
        zero_count = s.count("0")  # => co-18: an independent, brute-force parity check for cross-verification
        print(f"{s!r:<8} zeros={zero_count} accepted={actual} expected={expected}")  # => co-18: per-case report
        assert actual == expected, f"DFA verdict for {s!r} must be {expected}"  # => co-18: matches hand trace
        assert actual == (zero_count % 2 == 0), "DFA verdict must match brute-force zero-count parity"  # => co-18
    print(f"All test strings classified correctly: True")  # => co-18: every assert above passed
    # => co-18: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
