# Description text is scored by a deterministic fake selector.
def score(description: str, task: str) -> int:
    # Shared words approximate relevant model-facing evidence.
    return len(set(description.lower().split()) & set(task.lower().split()))


# The vague description does not mention the task.
vague = "Get information"
# The revised description gives the model a clear use case.
precise = "Search project notes by keyword"
# The task requests the precise operation.
task = "search notes"
# The revised contract supplies more selection evidence.
assert score(precise, task) > score(vague, task)
# Print the improvement measurement.
print(score(vague, task), score(precise, task))
