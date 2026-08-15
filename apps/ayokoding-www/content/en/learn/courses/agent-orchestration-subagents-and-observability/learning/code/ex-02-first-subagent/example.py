# A child receives detailed work in isolated state.
def subagent(task: str) -> str:
    # Only a compact outcome crosses back to the parent.
    return f"summary:{task}"


# The parent stores the returned summary only.
result = subagent("research")
# The contract makes the isolation observable.
assert result == "summary:research"
# Print the bounded return value.
print(result)
