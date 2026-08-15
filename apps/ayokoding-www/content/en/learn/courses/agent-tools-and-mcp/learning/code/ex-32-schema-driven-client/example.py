# Discovery returns server-owned field metadata.
schema = {"name": "weather", "required": ("city",)}


# The client builds a call from the discovered requirement.
def build(discovered: dict[str, object], value: str) -> dict[str, object]:
    # Read the field name instead of duplicating a local schema.
    field = discovered["required"][0]  # type: ignore[index]
    # Assemble the standard call shape from discovery.
    return {"name": discovered["name"], "args": {field: value}}


# A local value fills the server's advertised field.
call = build(schema, "Jakarta")
# The assertion proves no hard-coded city shape is needed.
assert call == {"name": "weather", "args": {"city": "Jakarta"}}
# Print the schema-driven call.
print(call)
