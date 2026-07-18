# learning/code/ex-28-red-green-refactor/tdd_cycle.py
"""Example 28: Red-Green-Refactor -- Three Sequential Diffs, One Passing Test."""  # => co-14: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-14: types the is_palindrome parameter run_test is quantified over
import difflib  # => co-14: difflib.unified_diff renders the actual PHASE-TO-PHASE diffs this example shows
from typing import cast  # => co-14: narrows exec()'s inherently untyped namespace lookup back to a known callable shape

RED_LINES = [  # => co-14: phase 1's source, as annotatable list items rather than one opaque triple-quoted blob
    "def is_palindrome(s: str) -> bool:",  # => co-14: phase 1 signature -- identical across all three phases
    '    raise NotImplementedError("not yet implemented")',  # => co-14: only the STUB exists -- the test cannot pass yet
]  # => co-14: closes the multi-line construct opened above

GREEN_LINES = [  # => co-14: phase 2's source -- the SMALLEST implementation that satisfies the fixed test below
    "def is_palindrome(s: str) -> bool:",  # => co-14: signature unchanged from RED
    '    cleaned = s.lower().replace(" ", "")',  # => co-14: strips spaces and case -- the minimal normalization needed
    "    return cleaned == cleaned[::-1]",  # => co-14: a full-string reversal comparison -- simple, not yet optimized
]  # => co-14: closes the multi-line construct opened above

REFACTOR_LINES = [  # => co-14: phase 3 -- cleaned up (handles punctuation, avoids a full reversed copy), same test still passes
    "def is_palindrome(s: str) -> bool:",  # => co-14: signature unchanged from GREEN
    '    cleaned = "".join(ch.lower() for ch in s if ch.isalnum())',  # => co-14: now also strips punctuation, not just spaces
    "    left, right = 0, len(cleaned) - 1",  # => co-14: two-pointer scan -- no reversed copy allocated
    "    while left < right:",  # => co-14: walks inward from both ends until the pointers meet
    "        if cleaned[left] != cleaned[right]:",  # => co-14: the first mismatch proves it is NOT a palindrome
    "            return False",  # => co-14: short-circuits the instant a mismatch is found
    "        left += 1",  # => co-14: advance the left pointer inward
    "        right -= 1",  # => co-14: advance the right pointer inward
    "    return True",  # => co-14: reached only if every pair matched -- IS a palindrome
]  # => co-14: closes the multi-line construct opened above

RED_SOURCE = "\n".join(RED_LINES) + "\n"  # => co-14: joins RED_LINES into one valid, exec-able Python source string
GREEN_SOURCE = "\n".join(GREEN_LINES) + "\n"  # => co-14: joins GREEN_LINES into one valid, exec-able Python source string
REFACTOR_SOURCE = "\n".join(REFACTOR_LINES) + "\n"  # => co-14: joins REFACTOR_LINES into one valid, exec-able Python source string


def make_callable(source: str) -> Callable[[str], bool]:  # => co-14: turns one phase's fixed, hardcoded local source into a callable
    """Exec one phase's fixed, hardcoded local source into an isolated namespace."""  # => co-14: documents make_callable's contract -- no runtime output, just sets its __doc__
    namespace: dict[str, object] = {}  # => co-14: an ISOLATED namespace -- nothing from this phase leaks into the next
    exec(source, namespace)  # => co-14: safe here -- source is one of the three fixed local strings above, never external input
    return cast(Callable[[str], bool], namespace["is_palindrome"])  # => co-14: hands back the function this phase's source just defined, typed for the caller


def run_test(is_palindrome: Callable[[str], bool]) -> tuple[bool, str]:  # => co-14: the ONE test -- never rewritten across red/green/refactor
    """The ONE test that stays fixed across all three phases."""  # => co-14: documents run_test's contract -- no runtime output, just sets its __doc__
    cases = {"racecar": True, "hello": False, "A man a plan a canal Panama": True}  # => co-14: a true palindrome, a non-palindrome, one with spaces/mixed case
    for text, expected in cases.items():  # => co-14: every case must agree, not just one
        actual = is_palindrome(text)  # => co-14: runs whichever phase's implementation was passed in
        if actual != expected:  # => co-14: the FIRST mismatch is enough to fail this phase
            return False, f"{text!r}: expected {expected}, got {actual}"  # => co-14: names the exact failing case
    return True, "all cases passed"  # => co-14: reached only if every case above matched


def print_diff(before: list[str], after: list[str], before_name: str, after_name: str) -> None:  # => co-14: one shared diff-printer, used for BOTH inter-phase diffs below
    """Print a real unified diff between two phases' source-line lists."""  # => co-14: documents print_diff's contract -- no runtime output, just sets its __doc__
    diff_lines = difflib.unified_diff(before, after, fromfile=before_name, tofile=after_name, lineterm="")  # => co-14: a REAL diff, computed from the fixed source lists above
    for line in diff_lines:  # => co-14: prints one diff line at a time, verbatim
        print(line)  # => co-14: the actual +/- diff hunk a reviewer would see between these two phases


if __name__ == "__main__":  # => co-14: entry point -- this block runs only when the file executes directly, not on import
    phases = [("RED", RED_SOURCE), ("GREEN", GREEN_SOURCE), ("REFACTOR", REFACTOR_SOURCE)]  # => co-14: the three phases, in order
    results: list[bool] = []  # => co-14: records PASS/FAIL for each phase, checked by the final assert
    for name, source in phases:  # => co-14: runs the SAME test against each phase's source in turn
        fn = make_callable(source)  # => co-14: materializes this phase's implementation
        try:  # => co-14: only RED is expected to raise -- GREEN and REFACTOR should return normally
            passed, message = run_test(fn)  # => co-14: runs the fixed test against this phase's implementation
        except NotImplementedError as exc:  # => co-14: expected ONLY during the RED phase's stub
            passed, message = False, f"raised NotImplementedError: {exc}"  # => co-14: treated as a failing result, not a crash
        results.append(passed)  # => co-14: collects this phase's pass/fail for the final assert
        print(f"--- {name} ---")  # => co-14: labels which phase this transcript block belongs to
        print(f"result: {'PASS' if passed else 'FAIL'} ({message})")  # => co-14: this phase's captured result

    print("\n--- diff: RED -> GREEN ---")  # => co-14: labels the first inter-phase diff
    print_diff(RED_LINES, GREEN_LINES, "red.py", "green.py")  # => co-14: shows exactly what the fix ADDED

    print("\n--- diff: GREEN -> REFACTOR ---")  # => co-14: labels the second inter-phase diff
    print_diff(GREEN_LINES, REFACTOR_LINES, "green.py", "refactor.py")  # => co-14: shows exactly what the refactor CHANGED

    assert results == [False, True, True], "expected RED to fail, GREEN and REFACTOR to pass"  # => co-14: the whole cycle's claim, checked
    print("\nRed failed, Green passed, Refactor still passes the same test: True")  # => co-14: this file is self-verifying -- a clean exit proves the claim held
