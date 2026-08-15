# A fixed budget models one agent's finite context.
budget = 5
# This task needs more detail than the parent can retain.
needed = 8
# The overflow is an explicit decision signal.
assert needed > budget
# Print the local limit result.
print("delegate")
