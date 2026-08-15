# Bounded research has a clear summary boundary.
def decide(task: str) -> str:
    # Final synthesis needs the parent-held full objective.
    return "delegate" if task == "research" else "keep"


# The two decisions model a deliberate split.
assert (decide("research"), decide("synthesis")) == ("delegate", "keep")
# Print the boundary decisions.
print(decide("research"), decide("synthesis"))
