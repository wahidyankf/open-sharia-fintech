# JSON-RPC-shaped records correlate a call with its response.
from dataclasses import dataclass


# A request carries an id, method, and typed params.
@dataclass(frozen=True)
class Request:
    # The id identifies the caller's pending operation.
    id: int
    # The method selects an advertised MCP tool.
    method: str
    # Params carry the structured tool arguments.
    params: dict[str, str]


# The local server returns a matching response record.
def handle(request: Request) -> dict[str, object]:
    # This simulation supports exactly one safe method.
    assert request.method == "tools/call"
    # Preserve the id so a client can match the response.
    return {"id": request.id, "result": f"hello, {request.params['name']}"}


# The request is deterministic and requires no transport.
response = handle(Request(1, "tools/call", {"name": "Ada"}))
# Matching id proves response correlation.
assert response == {"id": 1, "result": "hello, Ada"}
# Print the protocol-shaped response.
print(response)
