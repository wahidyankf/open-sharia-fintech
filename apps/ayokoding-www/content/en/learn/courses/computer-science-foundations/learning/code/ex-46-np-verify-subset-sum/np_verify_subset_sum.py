# learning/code/ex-46-np-verify-subset-sum/np_verify_subset_sum.py
"""Example 46: Verifying a Subset-Sum Certificate in Poly Time."""  # => co-24: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def verify_subset_sum(numbers: list[int], target: int, witness_indices: list[int]) -> bool:  # => co-24: the CHECKER
    """Verify a proposed witness (a set of indices) sums to target -- O(len(witness)), independent of len(numbers).

    This is NP's defining shape: VERIFYING a candidate solution is fast (poly-time), even though
    FINDING one in general is believed to require checking exponentially many candidate subsets.
    """  # => co-24: closes verify_subset_sum's docstring above -- no runtime output, just sets its __doc__
    # => co-24: the two paragraphs above spell out NP's defining VERIFY-fast-vs-FIND-hard asymmetry
    if len(set(witness_indices)) != len(witness_indices):  # => co-24: a witness may not reuse the same index twice
        return False  # => co-24: a malformed witness is rejected outright, not silently tolerated
    if any(i < 0 or i >= len(numbers) for i in witness_indices):  # => co-24: every index must be genuinely in range
        return False  # => co-24: an out-of-range witness is rejected
    return sum(numbers[i] for i in witness_indices) == target  # => co-24: the ENTIRE check -- one pass over the witness


if __name__ == "__main__":  # => co-24: entry point -- this block runs only when the file executes directly, not on import
    numbers = [3, 34, 4, 12, 5, 2]  # => co-24: the classic textbook subset-sum instance
    target = 9  # => co-24: is there a subset of `numbers` summing to exactly 9?
    valid_witness = [2, 4]  # => co-24: numbers[2]=4, numbers[4]=5 -- 4 + 5 = 9, a genuine solution
    invalid_witness = [0, 1]  # => co-24: numbers[0]=3, numbers[1]=34 -- 3 + 34 = 37, NOT 9
    accepts_valid = verify_subset_sum(numbers, target, valid_witness)  # => co-24: checker's verdict on a REAL witness
    rejects_invalid = not verify_subset_sum(numbers, target, invalid_witness)  # => co-24: verdict on a FAKE witness
    print(f"numbers={numbers} target={target}")  # => co-24: states the instance being checked
    print(f"valid witness {valid_witness} -> accepted: {accepts_valid}")  # => co-24: expect accepted
    print(f"invalid witness {invalid_witness} -> rejected: {rejects_invalid}")  # => co-24: expect rejected
    assert accepts_valid, "a genuine witness summing to the target must be accepted"  # => co-24
    assert rejects_invalid, "a witness NOT summing to the target must be rejected"  # => co-24
    malformed_witness = [1, 1]  # => co-24: the SAME index twice -- not a valid subset at all
    assert not verify_subset_sum(numbers, target, malformed_witness), "a repeated-index witness must be rejected"  # => co-24
    print(f"Checker accepts a valid witness and rejects invalid ones: True")  # => co-24: every assert above passed
    # => co-24: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
    # => co-24: the malformed-witness check above guards against a witness that "cheats" by reusing the same index twice
    # => co-24: verify_subset_sum runs in O(len(witness_indices)) time, independent of len(numbers) -- the defining trait of an NP verifier
