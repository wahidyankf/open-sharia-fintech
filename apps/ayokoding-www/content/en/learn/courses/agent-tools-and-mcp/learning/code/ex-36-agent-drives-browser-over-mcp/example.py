# The fake provider returns a deterministic browser observation.
def navigate(url: str) -> str:
    # A fixture URL prevents real network activity.
    assert url.startswith("https://example.test")
    # The title is a typed local result.
    return "Fixture"


# The loop invokes a discovered local capability.
assert navigate("https://example.test/") == "Fixture"
# Print the task result.
print(navigate("https://example.test/"))
