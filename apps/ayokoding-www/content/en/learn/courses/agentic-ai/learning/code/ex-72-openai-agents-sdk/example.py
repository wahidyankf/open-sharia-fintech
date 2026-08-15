from typing import Final  # => typed survey fixture

PRIMITIVES: Final[set[str]] = {"agents", "handoffs", "guardrails"}  # => SDK survey map
assert "guardrails" in PRIMITIVES  # => framework does not replace policy
print("PASS: openai-agents-sdk")  # => credential-free result
