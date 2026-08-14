def response(overloaded: bool) -> dict[str, object]:
    # Core redirect data stays available in both modes.
    result: dict[str, object] = {"destination": "https://example.test"}
    # Optional preview work is deliberately omitted under overload.
    if not overloaded:
        result["preview"] = "title and image"
    return result


assert "preview" in response(False) and "preview" not in response(True)
# The response shape makes degraded mode visible instead of silently losing data.
assert response(True)["destination"] == "https://example.test"
print(response(True))
