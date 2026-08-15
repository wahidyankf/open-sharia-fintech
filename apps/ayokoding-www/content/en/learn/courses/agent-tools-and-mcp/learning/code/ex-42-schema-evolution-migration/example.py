# Versioned input records make migrations explicit.
def migrate(call: dict[str, str]) -> dict[str, str]:
    # Version one used the old query field.
    if call["version"] == "1":
        return {"version": "2", "text": call["query"]}
    # Current calls already have the new shape.
    return call


# The old client input maps to the new schema.
assert migrate({"version": "1", "query": "notes"}) == {"version": "2", "text": "notes"}
# Print the migrated call.
print(migrate({"version": "1", "query": "notes"}))
