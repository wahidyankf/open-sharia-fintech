import os

key = os.environ.get(
    "AIAPP_KEY", "offline"
)  # => runtime environment seam; no secret is in source
assert key == "offline"  # => example runs without credentials
print("PASS: api-key-env")  # => offline acceptance result
