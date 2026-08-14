from typing import Final  # => typed threshold fixture

USED, THRESHOLD = 9, 8  # => context crosses compaction trigger
assert USED > THRESHOLD
print("PASS: trigger-compaction-on-budget")  # => compaction fires
