from typing import Final  # => typed survey fixture

VECTORS: Final[set[str]] = {"direct", "indirect"}  # => OWASP LLM01 forms
assert len(VECTORS) == 2  # => both boundaries need defense
print("PASS: owasp-llm01")  # => credential-free result
