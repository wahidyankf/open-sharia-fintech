"""Example 55: redact sensitive values before retaining a network trace."""

# => The fixture contains a secret-shaped value only to prove redaction behavior locally.
trace = {"url": "https://fixture.test/", "authorization": "fixture-secret"}
# => Replace the value before producing any diagnostic output.
safe_trace = {**trace, "authorization": "[REDACTED]"}
# => The retained trace exposes metadata while withholding the sensitive value.
assert safe_trace["authorization"] == "[REDACTED]"
# => Output is the redacted record suitable for a support trace.
print(safe_trace)
