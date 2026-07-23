"""Example 31: Four Ways -- Functional."""

from collections import Counter  # => way #3 of 4: a value-producing call, no visible mutation

sample = "red blue red green blue red"  # => identical sample to examples 29-30
result = dict(Counter(sample.split()))  # => one expression: tokenize, then fold into counts
print(result)  # => must match examples 29-30's dict exactly
# => Output: {'red': 3, 'blue': 2, 'green': 1}
