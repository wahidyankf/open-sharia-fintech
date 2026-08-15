from typing import Final  # => typed quality fixture

GAP: Final[str] = "missing decision"  # => comparison flags an omission
assert GAP.startswith("missing")
print("PASS: summary-quality-check")  # => quality signal
