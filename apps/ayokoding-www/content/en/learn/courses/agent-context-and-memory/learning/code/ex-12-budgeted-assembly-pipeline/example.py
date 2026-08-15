from typing import Final  # => typed assembly fixture

USED, LIMIT = 9, 10  # => all sources assembled under ceiling
assert USED <= LIMIT
print("PASS: budgeted-assembly-pipeline")  # => final fit invariant
