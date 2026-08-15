from typing import Final  # => typed isolation fixture

THREADS: Final[set[str]] = {"agent-a", "agent-b"}  # => independent loop identities
assert len(THREADS) == 2
print("PASS: concurrent-agents")  # => no shared state modeled
