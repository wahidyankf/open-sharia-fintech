# pyright: strict
"""Example 54: gRPC unary RPC -- request/response round-trip. (co-08)

gRPC uses Protocol Buffers as BOTH the interface-definition language and the
wire format, over HTTP/2. A UNARY RPC is one request -> one response. This
example simulates the protobuf service/handler in-process and verifies the
round-trip. Source: gRPC over HTTP/2 + Protobuf.
"""

from dataclasses import dataclass  # => a small typed record standing in for a protobuf message


@dataclass  # => co-08: a protobuf-message-like request
class EchoRequest:
    message: str  # => the payload the client sends


@dataclass  # => co-08: a protobuf-message-like response
class EchoResponse:
    message: str  # => the payload the server returns


class EchoService:  # => co-08: the gRPC service stub (stands in for generated code)
    def unary_echo(self, request: EchoRequest) -> EchoResponse:  # => co-08: a UNARY RPC -- one request, one response
        return EchoResponse(message=f"echo:{request.message}")  # => the single response


service = EchoService()  # => the server-side service instance
response = service.unary_echo(EchoRequest(message="hello"))  # => co-08: client sends one request
print(f"unary request:  {EchoRequest('hello')}")  # => Output: the request
print(f"unary response: {response}")  # => Output: one response
assert response.message == "echo:hello"  # => co-08: the request/response round-tripped
