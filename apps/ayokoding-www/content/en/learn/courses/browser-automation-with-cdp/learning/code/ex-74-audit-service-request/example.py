"""Example 74: create a minimal auditable browser-service request record."""

# => The record captures authorization, target, action, outcome, and correlation id.
audit = {
    "authorized": True,
    "target": "fixture.test",
    "action": "navigate",
    "outcome": "ok",
    "correlation_id": "run-8",
}
# => Required fields make the record useful without storing cookies or page content.
required = {"authorized", "target", "action", "outcome", "correlation_id"}
# => The assertion verifies a complete, secret-free audit shape.
assert set(audit) == required and audit["authorized"] is True
# => Output provides the structured audit evidence.
print(audit)
