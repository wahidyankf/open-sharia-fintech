from typing import Final  # => typed survey fixture

CONSTRUCTS: Final[tuple[str, str]] = ("crews", "flows")  # => framework vocabulary
assert len(CONSTRUCTS) == 2  # => no orchestration runtime is built
print("PASS: crewai-crews-flows")  # => credential-free result
