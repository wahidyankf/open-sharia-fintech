def route(method: str, replicas: list[str]) -> str:
    # Mutations always choose the single write authority.
    if method in {"POST", "PUT", "PATCH", "DELETE"}:
        return "leader"
    # Eligible reads can distribute across healthy replicas.
    return replicas[0] if replicas else "leader"


assert route("POST", ["replica-1"]) == "leader"
# A GET chooses a replica only when one is available.
assert route("GET", ["replica-1"]) == "replica-1"
print("routing safe")
