from typing import Final  # => typed cost fixture

TOKENS, COST = 100, 1  # => local context usage report
assert TOKENS == 100 and COST == 1
print("PASS: cost-of-context-report")  # => spend visible
