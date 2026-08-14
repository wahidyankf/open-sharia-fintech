# => Isolate the operation so its observable behavior can be checked.
def route(method: str, replicas: list[str]) -> str:
    # Mutations always choose the single write authority.
    # => Choose the branch that models this design condition.
    if method in {"POST", "PUT", "PATCH", "DELETE"}:
        # => Return the observable result of this modeled operation.
        return "leader"
    # Eligible reads can distribute across healthy replicas.
    # => Return the observable result of this modeled operation.
    return replicas[0] if replicas else "leader"


# => Check the promised observable behavior of the demonstration.
assert route("POST", ["replica-1"]) == "leader"
# A GET chooses a replica only when one is available.
# => Check the promised observable behavior of the demonstration.
assert route("GET", ["replica-1"]) == "replica-1"
# => Emit the final observable state for a direct run.
print("routing safe")
