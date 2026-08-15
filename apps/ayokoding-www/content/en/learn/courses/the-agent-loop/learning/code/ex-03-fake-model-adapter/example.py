from typing import Final  # => typed offline adapter fixture

TURN: Final[str] = "final"  # => canned deterministic response
assert TURN == "final"
print("PASS: fake-model-adapter")  # => no network
