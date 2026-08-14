# A small fixture has a low inline cost.
single_cost = 2
# Coordination adds overhead to the same simple work.
multi_cost = 5
# The comparison rejects orchestration by default.
assert single_cost < multi_cost
# Print the deliberate design choice.
print("single-agent")
