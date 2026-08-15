# A trace stores parent-child span relationships.
trace = {"run": ("turn", "tool")}
# The tree contains both observed child operations.
assert trace["run"] == ("turn", "tool")
# Print the local span tree.
print(trace)
