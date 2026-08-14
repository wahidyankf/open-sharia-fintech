from typing import Final  # => typed survey fixture

MEMORY: Final[dict[str, str]] = {"policy": "validate"}  # => retrievable prior fact
assert MEMORY.get("policy") == "validate"  # => relevant fact enters context
print("PASS: memory-retrieval")  # => credential-free result
