"""Example 70: retain a redacted, correlated failure transcript."""

# => A transcript preserves the command and error category needed for diagnosis.
transcript = {"correlation_id": "run-7", "method": "Page.navigate", "error": "timeout"}
# => Sensitive values are excluded, while timing and cause remain inspectable.
safe_keys = {"correlation_id", "method", "error"}
# => The assertion proves the retained record has exactly the approved evidence fields.
assert set(transcript) == safe_keys
# => Output is a deterministic failure record for a test assertion.
print(transcript)
