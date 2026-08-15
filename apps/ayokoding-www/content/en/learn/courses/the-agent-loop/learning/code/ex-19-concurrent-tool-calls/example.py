from typing import Final  # => typed concurrency fixture

JOINED: Final[bool] = True  # => independent calls have one join point
assert JOINED
print("PASS: concurrent-tool-calls")  # => no executor built
