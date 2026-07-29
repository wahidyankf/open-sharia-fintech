# pyright: strict
"""Example 55: gRPC server-streaming RPC. (co-08)

A server-streaming RPC takes ONE request and returns a STREAM of messages
(useful for a large or incrementally-produced result set). This example
simulates the stream as a generator and verifies multiple messages arrive
in order. Source: gRPC over HTTP/2.
"""

from collections.abc import Iterator  # => Iterator: the type of a streaming RPC's message stream
from dataclasses import dataclass  # => a small typed record standing in for a protobuf message


@dataclass  # => co-08: the streaming request (asks for N log lines)
class LogRequest:
    count: int  # => how many log lines the client wants


@dataclass  # => co-08: one streamed log-line message
class LogLine:
    seq: int  # => the sequence number of this line in the stream
    text: str  # => the line's content


class LogService:  # => co-08: the gRPC service with a server-streaming method
    def stream_logs(self, request: LogRequest) -> Iterator[LogLine]:  # => co-08: ONE request -> MANY streamed responses
        for seq in range(1, request.count + 1):  # => produce each line in order
            yield LogLine(seq=seq, text=f"log line {seq}")  # => one streamed message


service = LogService()  # => the server-side service
stream = service.stream_logs(LogRequest(count=4))  # => co-08: client sends one request
lines = list(stream)  # => collect every streamed message
for line in lines:  # => print them as they arrived
    print(f"received: seq={line.seq}, text={line.text!r}")  # => Output: 4 lines, in order

assert [line.seq for line in lines] == [1, 2, 3, 4]  # => co-08: multiple messages streamed back, in order
