# => Isolate the operation so its observable behavior can be checked.
def shard(identifier: int) -> str:
    # Ranges preserve ordering by assigning adjacent keys together.
    # => Return the observable result of this modeled operation.
    return "old" if identifier < 900 else "new"


# => Initialize or update deterministic state used by this demonstration.
recent = [shard(identifier) for identifier in range(900, 1_000)]
# Sequential recent IDs all land on one range and expose a hotspot.
# => Check the promised observable behavior of the demonstration.
assert set(recent) == {"new"}
# => Emit the final observable state for a direct run.
print("new range", len(recent))
