leader: dict[str, str] = {}
follower: dict[str, str] = {}


def write(key: str, value: str) -> None:
    # The leader accepts the authoritative write first.
    leader[key] = value


def replicate() -> None:
    # Replication is deliberately a separate step, exposing possible lag.
    follower.update(leader)


write("profile", "new")
# A follower is stale until the replication step occurs.
assert follower.get("profile") is None
replicate()
assert follower["profile"] == "new"
print("lag demonstrated")
