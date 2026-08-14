"""Example 23: block only an allowlisted fixture image request."""

# => The rule is narrow: it targets one synthetic image path, not all page traffic.
url = "https://fixture.test/ads/banner.png"
# => Interception makes a visible policy decision before a request would continue.
blocked = url.endswith("/ads/banner.png")
# => The assertion documents that this fixture request is intentionally blocked.
assert blocked is True
# => Output is auditable evidence of the rule decision.
print("blocked fixture image")
