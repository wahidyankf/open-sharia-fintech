from typing import Final  # => typed survey fixture

THREAD: Final[tuple[str, ...]] = ("question", "answer")  # => thread-local transcript
assert THREAD[0] == "question"  # => context remains scoped
print("PASS: short-term-memory")  # => credential-free result
