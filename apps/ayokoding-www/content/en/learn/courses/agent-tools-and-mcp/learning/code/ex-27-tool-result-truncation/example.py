# Result budgets prevent one call consuming future context.
def compact(text: str, limit: int) -> dict[str, object]:
    # Record whether data was omitted rather than hiding the loss.
    truncated = len(text) > limit
    # Return only the permitted prefix plus explicit metadata.
    return {"text": text[:limit], "truncated": truncated}


# A local oversized payload exercises the budget boundary.
result = compact("abcdefgh", 4)
# The flag lets a model decide whether to request more.
assert result == {"text": "abcd", "truncated": True}
# Print the compact observation.
print(result)
