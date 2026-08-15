from typing import Final  # => typed budget fixture

SPENT, CAP = 2, 2  # => cost policy state
assert SPENT <= CAP
print("PASS: budget-ceiling-stop")  # => stop boundary
