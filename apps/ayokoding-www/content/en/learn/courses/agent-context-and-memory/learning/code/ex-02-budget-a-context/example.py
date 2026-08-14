from typing import Final  # => typed budget fixture

USED, CEILING = 8, 10  # => assembled context must fit window
assert USED <= CEILING
print("PASS: budget-a-context")  # => fit invariant
