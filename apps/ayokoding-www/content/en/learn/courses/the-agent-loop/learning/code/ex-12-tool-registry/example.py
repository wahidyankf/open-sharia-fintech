from typing import Final  # => typed registry fixture

REGISTRY: Final[dict[str, str]] = {"echo": "callable"}  # => name mapping
assert REGISTRY["echo"] == "callable"
print("PASS: tool-registry")  # => lookup
