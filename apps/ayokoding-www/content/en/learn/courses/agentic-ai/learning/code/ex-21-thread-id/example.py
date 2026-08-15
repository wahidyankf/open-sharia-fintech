from typing import Final  # => typed survey fixture

THREADS: Final[set[str]] = {"a", "b"}  # => separate conversation scopes
assert len(THREADS) == 2  # => thread identity prevents mixing
print("PASS: thread-id")  # => credential-free result
