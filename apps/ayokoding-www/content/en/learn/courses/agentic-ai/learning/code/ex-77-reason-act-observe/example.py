from typing import Final  # => typed survey fixture

PHASES: Final[tuple[str, ...]] = ("reason", "act", "observe")  # => full bounded cycle
assert PHASES[-1] == "observe"  # => evidence informs next step
print("PASS: reason-act-observe")  # => credential-free result
