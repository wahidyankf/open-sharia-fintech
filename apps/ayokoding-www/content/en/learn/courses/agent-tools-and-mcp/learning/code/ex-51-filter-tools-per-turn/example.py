# A turn-specific task names the relevant capability.
tools = ("search", "write", "deploy")


# Filtering happens before a model chooses a tool.
def relevant(task: str) -> tuple[str, ...]:
    # Keep only tools whose names appear in the task.
    return tuple(tool for tool in tools if tool in task)


# This turn needs only the search contract.
filtered = relevant("search notes")
# The advertised surface is smaller than the full registry.
assert filtered == ("search",)
# Print the per-turn surface.
print(filtered)
