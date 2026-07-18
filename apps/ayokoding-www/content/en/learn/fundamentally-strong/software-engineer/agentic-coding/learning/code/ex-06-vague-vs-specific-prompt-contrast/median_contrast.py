# learning/code/ex-06-vague-vs-specific-prompt-contrast/median_contrast.py
"""Example ex-06: Vague vs. Specific Prompt Contrast -- Two Diffs, One Test."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


# --- VAGUE PROMPT: "write a median function" (no constraint on even-length input) --  # => co-05: the vague prompt's actual wording
def median_vague(values: list[float]) -> float:  # => co-05: FIRST diff -- generated from the vague prompt above
    """Return the median (vague-prompt version -- assumes odd length)."""  # => co-05: documents the contract this diff actually met
    ordered = sorted(values)  # => co-05: sorts ascending, same first step both versions share
    return ordered[len(ordered) // 2]  # => co-05: BUG for even length -- picks the upper-middle element only, never averages


# --- SPECIFIC PROMPT: goal + "for even-length input, average the two middle values" + example + AC --  # => co-05: the specific prompt's added constraint
def median_specific(values: list[float]) -> float:  # => co-05: SECOND diff -- generated from the specific prompt above
    """Return the median (specific-prompt version -- averages the two middles when length is even)."""  # => co-05: documents the contract this diff actually met
    ordered = sorted(values)  # => co-05: identical first step to the vague version
    mid = len(ordered) // 2  # => co-05: index of the (upper) middle element
    if len(ordered) % 2 == 0:  # => co-05: THE constraint the specific prompt added, now honored
        return (ordered[mid - 1] + ordered[mid]) / 2  # => co-05: average of the two true middle values
    return ordered[mid]  # => co-05: odd length -- the single true middle value, same as the vague version


if __name__ == "__main__":  # => co-05: entry point -- this block runs only when the file executes directly, not on import
    values: list[float] = [1, 2, 3, 4]  # => co-05: an EVEN-length case -- list[float] annotation needed since pyright infers bare [1, 2, 3, 4] as list[int], invariant vs the list[float] parameters
    expected = 2.5  # => co-05: the textbook median of [1, 2, 3, 4]
    vague_result = median_vague(values)  # => co-05: run the vague-prompt diff against the test case
    specific_result = median_specific(values)  # => co-05: run the specific-prompt diff against the same test case
    print(f"median_vague({values})    = {vague_result}  (expected {expected})")  # => co-05: shows the vague diff's answer
    print(f"median_specific({values}) = {specific_result}  (expected {expected})")  # => co-05: shows the specific diff's answer
    vague_passes = vague_result == expected  # => co-05: does the vague diff pass the test?
    specific_passes = specific_result == expected  # => co-05: does the specific diff pass the test?
    print(f"vague passes test: {vague_passes}")  # => co-05: expect False -- the vague diff's first-attempt bug
    print(f"specific passes test: {specific_passes}")  # => co-05: expect True -- the added constraint closed the gap
    assert vague_passes is False, "the vague prompt's first diff must NOT pass this even-length test"  # => co-05
    assert specific_passes is True, "the specific prompt's first diff must pass this even-length test"  # => co-05
    print("Specific prompt passes where vague prompt fails: True")  # => co-05: reached only if both asserts above passed
