"""Example 25: set a synthetic fixture cookie before navigation."""

# => Store only a fake test-session value; no credential or production cookie is involved.
cookies = {}
# => The cookie is scoped to the fixture origin that this course is authorized to model.
cookies[("https://fixture.test", "session")] = "test-session"
# => The page-facing lookup proves setup happened before the modeled navigation.
assert cookies[("https://fixture.test", "session")] == "test-session"
# => Output records the cookie name while keeping the value out of logs.
print("fixture cookie set: session")
