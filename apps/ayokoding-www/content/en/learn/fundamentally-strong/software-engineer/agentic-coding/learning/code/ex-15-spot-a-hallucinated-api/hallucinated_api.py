# learning/code/ex-15-spot-a-hallucinated-api/hallucinated_api.py
"""Example ex-15: Spot a Hallucinated API -- list.pop_front() Does Not Exist."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def hallucinated_pop_front(items: list[int]) -> int:  # => co-16: THE AGENT'S DIFF -- calls a plausible-sounding method Python's list never had
    """Remove and return the first element (agent's version -- calls a nonexistent method)."""  # => co-16: documents the (wrong) contract this diff claims to implement
    return items.pop_front()  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAttributeAccessIssue]  # => co-16: list.pop_front() does not exist in Python -- borrowed from a different language's API (e.g. JS Array, C++ deque); suppression is intentional, matching the deliberately-wrong-call convention at computer-science-foundations/.../huffman_lossless.py:51


def correct_pop_front(items: list[int]) -> int:  # => co-16: THE VERIFIED FIX -- the real stdlib call that does the same job
    """Remove and return the first element (the real API: list.pop(0))."""  # => co-16: documents the contract this diff actually implements
    return items.pop(0)  # => co-16: list.pop(index) IS a real method -- index 0 removes/returns the FIRST element


if __name__ == "__main__":  # => co-16: entry point -- this block runs only when the file executes directly, not on import
    data = [10, 20, 30]  # => co-16: shared test input for both the hallucinated call and its real replacement
    assert not hasattr(list, "pop_front"), "list must NOT have a pop_front method -- confirms this is a hallucination, not a typo"  # => co-16
    try:  # => co-16: this IS the verification step -- run the diff before trusting it, per co-13's discipline
        hallucinated_pop_front(list(data))  # => co-16: a fresh copy -- confirms the failure is the METHOD, not stale state
    except AttributeError as exc:  # => co-16: the exact exception Python raises for a nonexistent attribute/method
        print(f"hallucinated_pop_front() raised: {exc}")  # => co-16: the REAL captured error, proving the method never existed
    real_result = correct_pop_front(list(data))  # => co-16: a fresh copy again, run through the real, verified API
    print(f"correct_pop_front({data}) = {real_result}")  # => co-16: the correct result once the real API is used
    assert real_result == 10, "pop(0) must remove and return the first element"  # => co-16: confirms the fix behaves as claimed
    print("Hallucination caught before acceptance, real API confirmed working: True")  # => co-16: reached only if every assert above passed
