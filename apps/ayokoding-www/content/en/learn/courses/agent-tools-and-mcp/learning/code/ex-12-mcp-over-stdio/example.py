# Standard I/O can carry line-delimited JSON protocol messages.
import json


# Encoding turns an in-memory request into a transport line.
def encode(message: dict[str, object]) -> str:
    # A compact JSON string is safe to write to stdout.
    return json.dumps(message, separators=(",", ":"))


# Decoding turns the received line back into structured data.
def decode(line: str) -> dict[str, object]:
    # JSON parsing is the transport boundary's validation start.
    return json.loads(line)


# This record is the local stand-in for client stdout.
wire = encode({"id": 1, "method": "tools/list"})
# The server-side read recovers the same message shape.
assert decode(wire) == {"id": 1, "method": "tools/list"}
# Print the exact line a stdio peer would receive.
print(wire)
