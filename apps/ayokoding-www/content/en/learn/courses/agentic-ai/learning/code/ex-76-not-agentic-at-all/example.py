from typing import Final  # => typed survey fixture

NEEDS_AGENT: Final[bool] = False  # => ordinary code can be correct choice
assert not NEEDS_AGENT  # => restraint is explicit
print("PASS: not-agentic-at-all")  # => credential-free result
