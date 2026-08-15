# Depth is an explicit orchestration budget.
MAX_DEPTH = 2


# Delegation validates depth before starting another child.
def delegate(depth: int) -> str:
    # Reject depth beyond the bounded tree.
    return "allowed" if depth <= MAX_DEPTH else "rejected"


# The cap makes nested delegation finite.
assert (delegate(2), delegate(3)) == ("allowed", "rejected")
# Print the boundary result.
print(delegate(3))
