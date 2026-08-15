# The server validates independently of clients.
def list_items(limit: object) -> dict[str, object]:
    # Reject a non-positive integer at the executable boundary.
    if not isinstance(limit, int) or limit < 1:
        return {"ok": False, "code": "INVALID_LIMIT"}
    # Return a compact success shape after validation.
    return {"ok": True, "items": list(range(limit))}


# The malformed call produces typed feedback.
assert list_items(0) == {"ok": False, "code": "INVALID_LIMIT"}
# Print the client-visible validation error.
print(list_items(0))
