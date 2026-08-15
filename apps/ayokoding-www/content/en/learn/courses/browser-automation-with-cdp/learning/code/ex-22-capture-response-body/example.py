"""Example 22: capture an authorized, bounded local response body."""

# => The fixture body is synthetic and small enough to inspect without retaining real data.
body = '{"status":"ok"}'
# => Bound the capture before decoding so a large response cannot exhaust memory.
max_bytes = 64
# => UTF-8 byte length is the policy-relevant size for this JSON fixture.
assert len(body.encode("utf-8")) <= max_bytes
# => Output proves the approved fixture body passed the capture limit.
print(body)
