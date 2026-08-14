# A counter records names rather than sensitive arguments.
from collections import Counter

# The trace contains only tool identities.
trace = ["search", "search", "read"]
# Counting provides a compact usage measurement.
counts = Counter(trace)
# The measurement captures repeated search calls.
assert counts["search"] == 2
# Print the privacy-minimal metric.
print(dict(counts))
