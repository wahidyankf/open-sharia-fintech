# => Initialize or update deterministic state used by this demonstration.
leader: dict[str, str] = {}
# => Initialize or update deterministic state used by this demonstration.
follower: dict[str, str] = {}


# => Isolate the operation so its observable behavior can be checked.
def write(key: str, value: str) -> None:
    # The leader accepts the authoritative write first.
    # => Initialize or update deterministic state used by this demonstration.
    leader[key] = value


# => Isolate the operation so its observable behavior can be checked.
def replicate() -> None:
    # Replication is deliberately a separate step, exposing possible lag.
    # => Initialize or update deterministic state used by this demonstration.
    follower.update(leader)


# => Initialize or update deterministic state used by this demonstration.
write("profile", "new")
# A follower is stale until the replication step occurs.
# => Check the promised observable behavior of the demonstration.
assert follower.get("profile") is None
# => Initialize or update deterministic state used by this demonstration.
replicate()
# => Check the promised observable behavior of the demonstration.
assert follower["profile"] == "new"
# => Emit the final observable state for a direct run.
print("lag demonstrated")
