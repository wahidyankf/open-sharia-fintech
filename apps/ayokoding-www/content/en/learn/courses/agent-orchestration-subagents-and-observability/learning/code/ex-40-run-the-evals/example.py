# Fixture outcomes are booleans after grading.
outcomes = (True, True, False)
# The pass rate is computed from observed outcomes.
rate = sum(outcomes) / len(outcomes)
# The deterministic suite reports its evidence.
assert rate == 2 / 3
# Print the pass rate.
print(rate)
