# A resource is local read-only context.
policy = {"policy://reply": "Answer briefly."}
# Loading happens before the task response is formed.
context = policy["policy://reply"]
# The task uses supplied context instead of inventing policy.
answer = f"{context} Hello."
# The assertion shows resource data affected the task.
assert answer == "Answer briefly. Hello."
# Print the context-aware result.
print(answer)
