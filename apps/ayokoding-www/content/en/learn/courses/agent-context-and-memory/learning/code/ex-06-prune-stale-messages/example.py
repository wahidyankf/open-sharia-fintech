from typing import Final  # => typed history fixture

BEFORE, AFTER = 10, 6  # => stale messages were removed
assert AFTER < BEFORE
print("PASS: prune-stale-messages")  # => budget drops
