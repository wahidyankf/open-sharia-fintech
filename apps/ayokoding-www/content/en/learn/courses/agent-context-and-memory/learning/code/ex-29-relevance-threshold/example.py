from typing import Final  # => typed threshold fixture

SCORE, THRESHOLD = 2, 3  # => low candidate score and inclusion policy
assert SCORE < THRESHOLD
print("PASS: relevance-threshold")  # => noise excluded
