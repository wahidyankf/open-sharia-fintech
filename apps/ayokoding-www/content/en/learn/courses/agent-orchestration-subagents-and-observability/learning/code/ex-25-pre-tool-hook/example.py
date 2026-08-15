# A hook receives the request before the tool executes.
audit: list[str] = []


# The hook records minimal lifecycle evidence.
def before(name: str) -> None:
    audit.append(f"before:{name}")


# The dispatcher invokes the extension seam first.
before("search")
# The pre-call event is retained for review.
assert audit == ["before:search"]
# Print the hook audit.
print(audit)
