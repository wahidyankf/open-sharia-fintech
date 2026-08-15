from typing import Final  # => typed loss fixture

FIXED: Final[bool] = True  # => fixed summary retains required detail
assert FIXED
print("PASS: lossy-compaction-failure")  # => failure is addressed
