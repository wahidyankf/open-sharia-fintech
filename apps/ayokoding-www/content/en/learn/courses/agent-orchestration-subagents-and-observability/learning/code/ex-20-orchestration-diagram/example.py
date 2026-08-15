# This tuple is a compact text diagram of available patterns.
patterns = ("sequential", "parallel", "hierarchical")
# The source theme requires each named orchestration shape.
assert len(patterns) == 3
# Print the architecture labels.
print(" → ".join(patterns))
