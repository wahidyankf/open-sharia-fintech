# learning/code/ex-05-minimal-well-specified-prompt/is_clean_palindrome.py
"""Example ex-05: Minimal Well-Specified Prompt -- Prompt, Then Its Generated Diff."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

# --- THE PROMPT AS ACTUALLY GIVEN TO THE AGENT (co-05) ----------------------
# Goal: write a pure function is_clean_palindrome(s: str) -> bool.               # => co-05: states WHAT to build
# Constraints: no I/O, stdlib only, fully type-annotated (DD-39).                # => co-05: states the boundaries
# Example: is_clean_palindrome("A man, a plan, a canal: Panama") -> True.        # => co-05: pins down expected behavior
# Acceptance criteria:                                                          # => co-05: the bar the diff must clear
#   AC1. always returns bool, never None.                                       # => co-05: AC bullet 1
#   AC2. case-insensitive ("Racecar" passes).                                   # => co-05: AC bullet 2
#   AC3. ignores spaces and punctuation.                                        # => co-05: AC bullet 3
#   AC4. the empty string returns True.                                        # => co-05: AC bullet 4
# ------------------------------------------------------------------------------

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def is_clean_palindrome(s: str) -> bool:  # => co-05: THE GENERATED DIFF -- the agent's first response to the prompt above
    """Return whether `s` reads the same forwards/backwards, ignoring case/punctuation/spaces."""  # => co-05: documents the contract
    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())  # => co-05: AC2 (lower) + AC3 (isalnum drops space/punct) in one pass
    return cleaned == cleaned[::-1]  # => co-05: the palindrome check itself -- string equals its own reverse


if __name__ == "__main__":  # => co-05: entry point -- this block runs only when the file executes directly, not on import
    ac1 = is_clean_palindrome("Panama")  # => co-05: AC1 check target
    assert isinstance(ac1, bool), "AC1: must return a bool"  # => co-05: AC1 verified
    print(f"AC1 (returns bool): {isinstance(ac1, bool)}")  # pyright: ignore[reportUnnecessaryIsInstance]  # => co-05: prints AC1 result -- pyright already knows the declared return type is bool (that's WHY the assert above is unflagged), but this print restates the same runtime proof deliberately, so the suppression is intentional, not an oversight
    assert is_clean_palindrome("Racecar") is True, "AC2: case must be ignored"  # => co-05: AC2 verified
    print(f"AC2 (case-insensitive 'Racecar'): {is_clean_palindrome('Racecar')}")  # => co-05: prints AC2 result
    example = "A man, a plan, a canal: Panama"  # => co-05: the exact example named in the prompt
    assert is_clean_palindrome(example) is True, "AC3: punctuation/spaces must be ignored"  # => co-05: AC3 verified
    print(f"AC3 (ignores punctuation/spaces): {is_clean_palindrome(example)}")  # => co-05: prints AC3 result
    assert is_clean_palindrome("") is True, "AC4: empty string is vacuously a palindrome"  # => co-05: AC4 verified
    print(f"AC4 (empty string): {is_clean_palindrome('')}")  # => co-05: prints AC4 result
    print("All four acceptance-criteria bullets satisfied: True")  # => co-05: reached only if every assert above passed
