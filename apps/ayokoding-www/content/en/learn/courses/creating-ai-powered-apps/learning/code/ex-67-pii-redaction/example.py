import re

redacted = re.sub(
    r"[\w.+-]+@[\w.-]+", "[redacted]", "a@b.test"
)  # => remove email before logging
assert redacted == "[redacted]"  # => PII is absent from downstream text
print("PASS: pii-redaction")  # => offline acceptance result
