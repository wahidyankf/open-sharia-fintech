from typing import Final  # => typed usage fixture

TOKENS, COST = 10, 1  # => local summary metrics
assert TOKENS == 10 and COST == 1
print("PASS: cost-report")  # => reportable usage
