# learning/code/ex-34-nfa-nondeterminism/nfa_nondeterminism.py
"""Example 34: An NFA with epsilon-Moves -- Multiple Live States at Once."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

EPSILON = ""  # => co-18: the epsilon symbol -- a transition an NFA may take WITHOUT consuming any input
ALPHABET = ("a", "b", "x")  # => co-18: Σ for this machine -- "x" stands in for "any other character"


def epsilon_closure(states: set[str], transitions: dict[tuple[str, str], set[str]]) -> set[str]:  # => co-18
    """All states reachable from `states` using zero or more epsilon-moves."""  # => co-18: documents epsilon_closure's contract -- no runtime output, just sets its __doc__
    closure = set(states)  # => co-18: every starting state is trivially in its own closure
    frontier = list(states)  # => co-18: a worklist of states whose epsilon-moves still need exploring
    while frontier:  # => co-18: keep expanding until no NEW state is discovered via an epsilon-move
        state = frontier.pop()  # => co-18: take one state off the worklist
        for next_state in transitions.get((state, EPSILON), set()):  # => co-18: every epsilon-reachable neighbor
            if next_state not in closure:  # => co-18: only enqueue GENUINELY new states -- avoids infinite loops
                closure.add(next_state)  # => co-18: newly discovered -- now part of the closure
                frontier.append(next_state)  # => co-18: and its OWN epsilon-moves must be explored too
    return closure  # => co-18: returns this computed value to the caller


def run_nfa(  # => co-18: an NFA tracks a SET of live states, unlike a DFA's single current state
    s: str,  # => co-18: one parameter of the multi-line signature above
    transitions: dict[tuple[str, str], set[str]],  # => co-18: one parameter of the multi-line signature above
    start: str,  # => co-18: one parameter of the multi-line signature above
    accept: set[str],  # => co-18: one parameter of the multi-line signature above
) -> bool:  # => co-18: continues the statement started above
    """Run an NFA on input s; True iff at least one live state after epsilon-closure is accepting."""  # => co-18: documents the routine above's contract -- no runtime output, just sets its __doc__
    live: set[str] = epsilon_closure({start}, transitions)  # => co-18: MULTIPLE states can be live from the start
    for symbol in s:  # => co-18: one non-epsilon step per input symbol
        next_live: set[str] = set()  # => co-18: the NEW set of live states after consuming this symbol
        for state in live:  # => co-18: every CURRENTLY live state may branch on this symbol independently
            next_live |= transitions.get((state, symbol), set())  # => co-18: union -- nondeterminism means MANY branches
        live = epsilon_closure(next_live, transitions)  # => co-18: expand epsilon-moves after every real symbol too
    return bool(live & accept)  # => co-18: accept iff ANY live state (not all) is an accepting state


if __name__ == "__main__":  # => co-18: entry point -- this block runs only when the file executes directly, not on import
    # ex-34: NFA accepting strings containing "ab" as a substring -- deliberately messy for a DFA to
    # express directly with this exact shape, but trivial for an NFA: guess (via epsilon) where "ab" starts
    transitions: dict[tuple[str, str], set[str]] = {  # => co-18: q0 stays via self-loops OR epsilon-guesses q1
        **{("q0", sym): {"q0"} for sym in ALPHABET},  # => co-18: q0: consume ANY symbol, keep "still waiting"
        ("q0", EPSILON): {"q1"},  # => co-18: NONDETERMINISM: q0 may ALSO, for free, guess "the 'ab' starts now"
        ("q1", "a"): {"q2"},  # => co-18: q1: committed to seeing "a" next
        ("q2", "b"): {"q3"},  # => co-18: q2: committed to seeing "b" next -- reaching q3 means "ab" was found
        **{("q3", sym): {"q3"} for sym in ALPHABET},  # => co-18: q3: accepting, and stays accepting for any suffix
    }  # => co-18: closes the multi-line construct opened above
    accept = {"q3"}  # => co-18: F -- only q3 accepts
    test_cases = {"ab": True, "xab": True, "abx": True, "aabb": True, "aaa": False, "": False}  # => co-18
    for s, expected in test_cases.items():  # => co-18: run every case through the NFA simulator
        actual = run_nfa(s, transitions, "q0", accept)  # => co-18: multiple live states are tracked internally
        contains_ab = "ab" in s  # => co-18: an independent brute-force check for cross-verification
        print(f"{s!r:<6} accepted={actual} expected={expected} contains_ab={contains_ab}")  # => co-18
        assert actual == expected == contains_ab, f"NFA verdict for {s!r} must match hand trace"  # => co-18
    print(f"NFA correctly tracks multiple live states via nondeterminism: True")  # => co-18: all asserts passed
    # => co-18: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
