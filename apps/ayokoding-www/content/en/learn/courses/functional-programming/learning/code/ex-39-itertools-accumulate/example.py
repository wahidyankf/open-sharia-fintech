"""Example 39: Running Totals via accumulate."""

from itertools import (
    accumulate,
)  # => a lazy iterator of running totals (or any binary op)

deposits = [100, 50, -30, 200]  # => a sequence of account movements

running_balance = list(
    accumulate(deposits)
)  # => default op is +: each step is the sum SO FAR
running_max = list(
    accumulate(deposits, max)
)  # => a custom op: running maximum instead of sum
# => accumulate is itertools' generalized fold-that-keeps-every-intermediate-result

print(running_balance)  # => Output: [100, 150, 120, 320]
print(running_max)  # => Output: [100, 100, 100, 200]
print(
    running_balance[-1] == sum(deposits)
)  # => Output: True -- the LAST running total is the full sum
