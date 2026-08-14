# A typed request separates a model proposal from execution.
from dataclasses import dataclass


# The model returns a name plus structured arguments.
@dataclass(frozen=True)
class Call:
    name: str
    args: dict[str, int]


# Dispatch maps an allowed name to deterministic code.
def dispatch(call: Call) -> dict[str, int]:
    # Only the known sum contract is executable here.
    assert call.name == "sum"
    # The result becomes a typed observation for the loop.
    return {"value": call.args["a"] + call.args["b"]}


# A fake model request requires neither a key nor a network call.
result = dispatch(Call("sum", {"a": 2, "b": 3}))
# The assertion proves the whole request-execute-result round trip.
assert result == {"value": 5}
# Print the observation the model would receive next.
print(result)
