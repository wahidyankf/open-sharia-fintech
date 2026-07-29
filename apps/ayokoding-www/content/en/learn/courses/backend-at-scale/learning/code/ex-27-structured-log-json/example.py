# pyright: strict
"""Example 27: Structured Logging -- a JSON line with typed fields. (co-25)

A structured log is a machine-parseable JSON object with typed fields
(timestamp, level, message, request_id) rather than free text. This example
emits one such line and verifies it parses back to a dict with the expected
keys -- so a downstream log aggregator can index every field.
"""

import json  # => stdlib: serialize the record to a JSON line and parse it back


def log_json(level: str, message: str, request_id: str, timestamp: str = "2026-07-29T10:00:00Z") -> str:
    # => co-25: every field is a TYPED value, not interpolated prose
    record: dict[str, str] = {  # => the structured fields
        "timestamp": timestamp,  # => when the event happened (ISO-8601)
        "level": level,  # => severity: info/warn/error
        "message": message,  # => a short human-readable summary
        "request_id": request_id,  # => co-25: the correlation key tying this line to one request
    }
    return json.dumps(record)  # => one JSON line, ready for a log shipper to ingest


line = log_json(level="info", message="order created", request_id="req-abc-123")  # => emit one structured line
print(line)  # => Output: a single JSON object on one line

parsed = json.loads(line)  # => co-25: verify it round-trips into a parseable dict
print(f"parsed message: {parsed['message']}")  # => Output: order created

expected_keys = {"timestamp", "level", "message", "request_id"}  # => the typed fields every line carries
assert set(parsed.keys()) == expected_keys  # => co-25: the line parses with exactly these fields
assert parsed["level"] == "info" and parsed["request_id"] == "req-abc-123"  # => fields are typed values
