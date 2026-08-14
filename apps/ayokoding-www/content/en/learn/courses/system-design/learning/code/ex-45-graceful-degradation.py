# => Isolate the operation so its observable behavior can be checked.
def response(overloaded: bool) -> dict[str, object]:
    # Core redirect data stays available in both modes.
    # => Initialize or update deterministic state used by this demonstration.
    result: dict[str, object] = {"destination": "https://example.test"}
    # Optional preview work is deliberately omitted under overload.
    # => Choose the branch that models this design condition.
    if not overloaded:
        # => Initialize or update deterministic state used by this demonstration.
        result["preview"] = "title and image"
    # => Return the observable result of this modeled operation.
    return result


# => Check the promised observable behavior of the demonstration.
assert "preview" in response(False) and "preview" not in response(True)
# The response shape makes degraded mode visible instead of silently losing data.
# => Check the promised observable behavior of the demonstration.
assert response(True)["destination"] == "https://example.test"
# => Emit the final observable state for a direct run.
print(response(True))
