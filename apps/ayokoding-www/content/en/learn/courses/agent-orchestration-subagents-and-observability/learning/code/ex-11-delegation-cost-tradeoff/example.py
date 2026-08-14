# Inline work has no coordination handoff in this model.
inline_cost = 3
# Delegation includes task setup and summary transfer.
delegated_cost = 5
# The comparison makes overhead explicit.
assert delegated_cost > inline_cost
# Print the measured local trade-off.
print({"inline": inline_cost, "delegated": delegated_cost})
