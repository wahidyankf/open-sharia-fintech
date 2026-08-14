# The coordinator owns high-level lifecycle steps.
trace = ["plan"]
# Dispatch hands bounded tasks to workers.
trace.append("dispatch")
# Collect brings summaries back to the coordinator.
trace.append("collect")
# The lifecycle shows hierarchical ownership.
assert trace == ["plan", "dispatch", "collect"]
# Print the orchestration trace.
print(trace)
