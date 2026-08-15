from typing import Final  # => typed survey fixture

PLAN: Final[tuple[str, ...]] = ("lookup", "summarize")  # => proposed bounded sequence
assert len(PLAN) == 2  # => plan is explicit data
print("PASS: plan-and-execute")  # => credential-free result
