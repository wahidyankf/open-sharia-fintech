# This tuple is a text-only local diagram artifact.
flow = ("parent", "task", "subagent", "summary", "parent")
# The child receives work and returns a summary only.
assert flow[1:4] == ("task", "subagent", "summary")
# Print the directional information flow.
print(" → ".join(flow))
