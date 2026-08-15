"""Example 58: classify a protocol failure before selecting recovery."""

# => The fixture error carries a stable category, not only an opaque exception string.
error = {"kind": "target-lost", "retryable": True}
# => Recovery policy derives from the category and can therefore be unit-tested.
action = "reattach" if error["kind"] == "target-lost" else "fail"
# => The assertion maps a lost target to explicit reattachment behavior.
assert action == "reattach" and error["retryable"] is True
# => Output makes the chosen recovery path inspectable.
print(action)
