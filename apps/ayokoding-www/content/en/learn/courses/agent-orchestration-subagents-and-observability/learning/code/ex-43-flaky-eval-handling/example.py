# Multiple samples model stochastic evaluator outcomes.
samples = (True, True, True, True, False)
# A threshold states the required repeatable success ratio.
threshold = 0.8
# The aggregate rule avoids trusting a single sample.
rate = sum(samples) / len(samples)
# Four of five local samples meet the threshold.
assert rate >= threshold
# Print the robust pass rate.
print(rate)
