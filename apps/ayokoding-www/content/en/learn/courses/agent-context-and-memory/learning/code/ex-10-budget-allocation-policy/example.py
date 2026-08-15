from typing import Final  # => typed allocation fixture

SPLIT: Final[dict[str, int]] = {
    "memory": 20,
    "retrieval": 40,
    "history": 40,
}  # => budget policy
assert sum(SPLIT.values()) == 100
print("PASS: budget-allocation-policy")  # => complete split
