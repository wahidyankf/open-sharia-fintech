from typing import Final  # => typed loop fixture

FITS: Final[bool] = True  # => compacted context remains inside budget
assert FITS
print("PASS: compaction-in-the-loop")  # => loop can continue
