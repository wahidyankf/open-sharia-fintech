# This tool validates before returning a bounded result.
def search(query: object) -> dict[str, object]:
    # Invalid model data becomes an explicit error shape.
    if not isinstance(query, str) or not query:
        return {"ok": False, "code": "INVALID_QUERY"}
    # The result exposes only one safe local hit.
    return {"ok": True, "hits": [query][:1]}


# The hostile empty input exercises the boundary.
assert search("")["code"] == "INVALID_QUERY"
# Print the safe error observation.
print(search(""))
