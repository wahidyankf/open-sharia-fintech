"""Example 45: from ... import."""

from statistics import mean  # => imports just the one name, used unqualified below

print(mean([1, 2, 3]))  # => (1+2+3)/3 = 2 -- Output: 2
