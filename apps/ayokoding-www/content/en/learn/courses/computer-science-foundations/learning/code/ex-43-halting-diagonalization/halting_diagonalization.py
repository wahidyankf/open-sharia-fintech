# learning/code/ex-43-halting-diagonalization/halting_diagonalization.py
"""Example 43: The Halting-Problem Diagonalization Contradiction, Sketched in Code."""  # => co-23: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

# ex-43: Turing's 1936 argument, sketched mechanically. Suppose a halting oracle H(P, I) exists,
# deciding whether program P halts on input I. Define D(P): "if H(P, P) says P halts, loop
# forever; otherwise, halt." The contradiction appears the instant D is applied to ITSELF (co-23).


def d_behavior_given_oracle_answer(oracle_says_p_halts_on_itself: bool) -> str:  # => co-23: D's OWN definition
    """D(P)'s behavior, defined directly in terms of what a hypothetical oracle H(P, P) claims."""  # => co-23: documents d_behavior_given_oracle_answer's contract -- no runtime output, just sets its __doc__
    if oracle_says_p_halts_on_itself:  # => co-23: D's definition: "if H(P, P) says halts..."
        return "LOOPS_FOREVER"  # => co-23: "...then loop forever" -- D deliberately defies the oracle's answer
    return "HALTS"  # => co-23: "...otherwise, halt" -- D again defies the oracle's answer


if __name__ == "__main__":  # => co-23: entry point -- this block runs only when the file executes directly, not on import
    # Apply D to ITSELF (P := D) -- exactly the diagonalization move. A real oracle H would have
    # to answer H(D, D) with EITHER True (halts) or False (loops forever) -- there is no third option.
    oracle_claims_true = True  # => co-23: CASE 1 -- suppose the (hypothetical) oracle claims "D(D) halts"
    actual_behavior_if_true = d_behavior_given_oracle_answer(oracle_claims_true)  # => co-23: D's OWN definition
    contradiction_1 = actual_behavior_if_true == "LOOPS_FOREVER"  # => co-23: oracle said "halts", D actually loops
    print(f"oracle claims D(D) halts -> D's own definition makes it: {actual_behavior_if_true}")  # => co-23

    oracle_claims_false = False  # => co-23: CASE 2 -- suppose the oracle instead claims "D(D) loops forever"
    actual_behavior_if_false = d_behavior_given_oracle_answer(oracle_claims_false)  # => co-23: D's OWN definition
    contradiction_2 = actual_behavior_if_false == "HALTS"  # => co-23: oracle said "loops", D actually halts
    print(f"oracle claims D(D) loops -> D's own definition makes it: {actual_behavior_if_false}")  # => co-23

    assert contradiction_1, "if the oracle claims 'halts', D's own definition must make it loop"  # => co-23
    assert contradiction_2, "if the oracle claims 'loops', D's own definition must make it halt"  # => co-23
    print("Every possible oracle answer contradicts D's own defined behavior: True")  # => co-23
    print("No H(P, I) can exist that answers correctly for every (P, I) -- the halting problem is undecidable.")  # => co-23: continues the statement started above
    # => co-23: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
