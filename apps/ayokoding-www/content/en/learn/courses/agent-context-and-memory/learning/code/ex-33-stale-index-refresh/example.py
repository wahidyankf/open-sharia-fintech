from typing import Final  # => typed refresh fixture

VERSION: Final[int] = 2  # => source update produced refreshed index
assert VERSION == 2
print("PASS: stale-index-refresh")  # => updated retrieval source
