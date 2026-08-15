# Two providers own independent capability maps.
notes = {"read": lambda: "note"}
# A second provider can coexist without a shared implementation.
status = {"health": lambda: "ok"}
# The client composes only the discovered calls it needs.
result = {"note": notes["read"](), "health": status["health"]()}
# Both results remain attributable to their source.
assert result == {"note": "note", "health": "ok"}
# Print the composed observation.
print(result)
