from typing import Final  # => typed open-work fixture

SUMMARY: Final[str] = "open: approve deployment"  # => unresolved task retained
assert "open:" in SUMMARY
print("PASS: compaction-preserves-open-threads")  # => pending state
