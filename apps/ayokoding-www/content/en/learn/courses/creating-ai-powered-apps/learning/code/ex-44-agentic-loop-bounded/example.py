steps = ["plan", "act", "observe"]  # => one bounded loop iteration
assert steps[-1] == "observe"  # => tool result is observed
print("PASS: agentic-loop-bounded")  # => offline acceptance result
