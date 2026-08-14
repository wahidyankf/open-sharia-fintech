from typing import Final  # => typed policy fixture

FACTS: Final[tuple[str, ...]] = (
    "prefers dark mode",
    "um",
    "prefers short answers",
)  # => candidate notes
remembered: tuple[str, ...] = tuple(
    fact for fact in FACTS if fact.startswith("prefers")
)  # => durable-only policy
assert "um" not in remembered
print("PASS: memory-write-policy")  # => noise excluded
