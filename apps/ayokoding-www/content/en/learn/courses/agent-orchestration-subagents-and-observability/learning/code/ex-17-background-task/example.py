# A background task exposes a pollable state.
state = "pending"
# The main interaction can inspect the initial state.
assert state == "pending"
# The local worker later completes independently.
state = "done"
# Polling observes the completed lifecycle state.
assert state == "done"
# Print the final background status.
print(state)
