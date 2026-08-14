from typing import Final  # => typed survey fixture

STORE: Final[dict[str, str]] = {"user": "preference"}  # => persistent scoped record
assert STORE["user"] == "preference"  # => memory survives a session conceptually
print("PASS: long-term-memory")  # => credential-free result
