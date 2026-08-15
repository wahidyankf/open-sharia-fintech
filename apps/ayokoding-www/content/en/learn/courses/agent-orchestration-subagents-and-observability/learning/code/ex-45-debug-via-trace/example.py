# A trace records the decisive failed operation.
trace = ("plan", "wrong-tool", "error")
# Diagnosis finds the failure without replaying work.
cause = trace[1]
# The trace supports a concrete root-cause claim.
assert cause == "wrong-tool"
# Print the diagnosed cause.
print(cause)
