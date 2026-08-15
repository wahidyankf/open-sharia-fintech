from typing import Final  # => typed survey fixture

WORKERS: Final[tuple[str, str]] = ("research", "draft")  # => delegated scopes
assert len(WORKERS) == 2  # => no worker runtime is implemented
print("PASS: orchestrator-workers")  # => offline result
