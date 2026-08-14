# => Isolate the operation so its observable behavior can be checked.
def overlaps(replicas: set[str], written: set[str], read: set[str]) -> bool:
    # A read can see a completed write only if their replica sets intersect.
    # => Return the observable result of this modeled operation.
    return written <= replicas and read <= replicas and bool(written & read)


# => Initialize or update deterministic state used by this demonstration.
nodes = {"a", "b", "c"}
# W=2 and R=2 over N=3 must share at least one replica.
# => Check the promised observable behavior of the demonstration.
assert overlaps(nodes, {"a", "b"}, {"b", "c"})
# => Emit the final observable state for a direct run.
print("quorum overlap")
