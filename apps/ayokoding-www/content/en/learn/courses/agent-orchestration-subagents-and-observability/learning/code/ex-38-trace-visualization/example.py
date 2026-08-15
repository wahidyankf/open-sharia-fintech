# A local text diagram names nested spans.
flow = ("run", "subagent", "tool")
# The diagram preserves causal hierarchy.
assert flow[0] == "run" and flow[-1] == "tool"
# Print the span visualization.
print(" → ".join(flow))
