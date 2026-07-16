# learning/code/ex-33-dfa-simulator/dfa_simulator.py
"""Example 33: A Generic DFA Driven by a Transition Table."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from dataclasses import dataclass  # => co-18: a typed, reusable DFA definition -- states, alphabet, delta


@dataclass(frozen=True)  # => co-18: a DFA is DATA -- five components, per the formal (Q, Σ, δ, q0, F) definition
class Dfa:  # => co-18: this SAME class drives any DFA supplied to it -- the "generic simulator" this example is
    states: frozenset[str]  # => co-18: Q -- the finite set of states
    alphabet: frozenset[str]  # => co-18: Σ -- the finite input alphabet
    transitions: dict[tuple[str, str], str]  # => co-18: δ -- (state, symbol) -> next state
    start: str  # => co-18: q0 -- the single designated start state
    accept: frozenset[str]  # => co-18: F -- the subset of states that accept

    def run(self, s: str) -> bool:  # => co-18: feeds `s` through δ symbol by symbol, from q0
        """Run this DFA on input string s; True iff it ends in an accepting state."""  # => co-18: documents run's contract -- no runtime output, just sets its __doc__
        state = self.start  # => co-18: begins at q0, every run, unconditionally
        for symbol in s:  # => co-18: one transition per symbol -- a DFA has exactly one next state per step
            if symbol not in self.alphabet:  # => co-18: outside Σ is undefined for THIS machine
                raise ValueError(f"{symbol!r} not in alphabet {sorted(self.alphabet)}")  # => co-18: fail loudly
            state = self.transitions[(state, symbol)]  # => co-18: δ(state, symbol) -- the ONE next state
        return state in self.accept  # => co-18: accepted iff the FINAL state is in F


if __name__ == "__main__":  # => co-18: entry point -- this block runs only when the file executes directly, not on import
    # ex-33: a DIFFERENT machine than Example 32 -- this DFA accepts binary strings ENDING in "1"
    ends_in_one = Dfa(  # => co-18: proves the simulator is generic by running a machine Example 32 never defined
        states=frozenset({"S0", "S1"}),  # => co-18: S0 = "last symbol was 0 or start", S1 = "last symbol was 1"
        alphabet=frozenset({"0", "1"}),  # => co-18: Σ
        transitions={  # => co-18: δ -- the full transition table for this machine
            ("S0", "0"): "S0",  # => co-18: from S0, "0" stays at S0 -- last symbol still not "1"
            ("S0", "1"): "S1",  # => co-18: from S0, "1" moves to S1 -- last symbol is now "1"
            ("S1", "0"): "S0",  # => co-18: from S1, "0" moves back to S0 -- last symbol is now "0"
            ("S1", "1"): "S1",  # => co-18: from S1, "1" stays at S1 -- last symbol still "1"
        },  # => co-18: closes the multi-line construct opened above
        start="S0",  # => co-18: q0
        accept=frozenset({"S1"}),  # => co-18: F -- accept iff the string's last symbol was "1"
    )  # => co-18: closes the multi-line construct opened above
    test_cases = {"1": True, "0": False, "101": True, "110": False, "": False}  # => co-18: hand-traced expectations
    for s, expected in test_cases.items():  # => co-18: run every case through the generic simulator
        actual = ends_in_one.run(s)  # => co-18: the SAME Dfa.run() method Example 32's machine would also use
        print(f"{s!r:<5} accepted={actual} expected={expected}")  # => co-18: per-case report
        assert actual == expected, f"verdict for {s!r} must match hand-traced expectation"  # => co-18
    print(f"Generic simulator correctly runs a supplied machine: True")  # => co-18: every assert above passed
    # => co-18: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
