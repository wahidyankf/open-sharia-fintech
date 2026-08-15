from typing import Final  # => typed survey fixture

ATTRIBUTE: Final[str] = "gen_ai.operation.name"  # => structured trace key
assert ATTRIBUTE.startswith("gen_ai.")  # => semantic namespace is visible
print("PASS: tracing-attributes")  # => credential-free result
