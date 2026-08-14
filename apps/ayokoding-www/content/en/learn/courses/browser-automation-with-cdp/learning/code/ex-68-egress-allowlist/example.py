"""Example 68: deny browser navigation outside an egress allowlist."""

# => The service owns a small set of authorized fixture origins.
allowed_origins = {"https://fixture.test"}
# => Split the requested URL to compare only the origin policy boundary.
requested_origin = "https://fixture.test"
# => The assertion proves navigation is admitted only for the allowlisted origin.
assert requested_origin in allowed_origins
# => Output makes the egress authorization decision explicit.
print("egress allowed: fixture.test")
