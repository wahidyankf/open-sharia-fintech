def overlaps(replicas: set[str], written: set[str], read: set[str]) -> bool:
    # A read can see a completed write only if their replica sets intersect.
    return written <= replicas and read <= replicas and bool(written & read)


nodes = {"a", "b", "c"}
# W=2 and R=2 over N=3 must share at least one replica.
assert overlaps(nodes, {"a", "b"}, {"b", "c"})
print("quorum overlap")
