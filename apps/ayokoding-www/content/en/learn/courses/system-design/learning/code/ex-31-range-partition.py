def shard(identifier: int) -> str:
    # Ranges preserve ordering by assigning adjacent keys together.
    return "old" if identifier < 900 else "new"


recent = [shard(identifier) for identifier in range(900, 1_000)]
# Sequential recent IDs all land on one range and expose a hotspot.
assert set(recent) == {"new"}
print("new range", len(recent))
