"""Example 66: enforce a narrow request-interception policy."""

# => The policy allows one explicit fixture action for one known resource pattern.
policy = {"suffix": "/ads/banner.png", "action": "block"}
# => Evaluate the request against that allowlisted pattern before changing behavior.
url = "https://fixture.test/ads/banner.png"
# => The assertion proves only the matching fixture request is blocked.
assert url.endswith(policy["suffix"]) and policy["action"] == "block"
# => Output records the policy decision for an audit trail.
print("fixture request blocked by policy")
