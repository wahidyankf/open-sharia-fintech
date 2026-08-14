from typing import Final  # => typed survey fixture

TRAJECTORY: Final[tuple[str, ...]] = (
    "lookup",
    "answer",
)  # => observable action sequence
assert TRAJECTORY[-1] == "answer"  # => deep scoring is forward-linked
print("PASS: trajectory-eval")  # => offline result
