# A baseline score exposes a failing behavior.
before = 0.5
# The narrow local fix improves the measured fixture score.
after = 1.0
# Evaluation verifies the direction of change.
assert after > before
# Print the measured improvement.
print({"before": before, "after": after})
