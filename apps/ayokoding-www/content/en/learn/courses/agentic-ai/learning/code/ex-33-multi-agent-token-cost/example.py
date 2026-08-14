from typing import Final  # => typed survey fixture

TOKENS: Final[int] = 15  # => multi-agent cost multiplier fixture
assert TOKENS > 1  # => coordination is not free
print("PASS: multi-agent-token-cost")  # => offline result
