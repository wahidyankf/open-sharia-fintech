# Human approval is represented separately from model intent.
approved = False
# The action gate checks the external decision.
result = "run" if approved else "blocked"
# A denied prompt cannot dispatch the action.
assert result == "blocked"
# Print the approval outcome.
print(result)
