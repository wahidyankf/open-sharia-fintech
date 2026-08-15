from typing import Final  # => typed durable-store fixture

MEMORY: Final[dict[str, str]] = {"preference": "concise"}  # => shared across sessions
new_session: dict[str, str] = MEMORY.copy()  # => simulated recall
assert new_session["preference"] == "concise"
print("PASS: persist-long-term-memory")  # => recalled later
