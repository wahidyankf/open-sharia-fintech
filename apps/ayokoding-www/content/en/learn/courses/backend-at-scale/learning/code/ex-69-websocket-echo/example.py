# pyright: strict
"""Example 69: WebSocket echo -- a bidirectional round-trip. (co-33)

WebSocket is a full-duplex, bidirectional protocol over ONE TCP connection
(RFC 6455, 2011). This example simulates a single persistent connection where
the client sends a frame and the server echoes it back over the SAME channel.
"""

from collections import deque  # => deque: the bidirectional channel's two directions
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-33: one message frame on the connection
class Frame:
    payload: str  # => the frame's content


@dataclass  # => co-33: a full-duplex connection with a client->server and server->client direction
class WebSocket:
    to_server: deque[Frame] = field(default_factory=deque[Frame])  # => client -> server frames
    to_client: deque[Frame] = field(default_factory=deque[Frame])  # => server -> client frames

    def client_send(self, frame: Frame) -> None:  # => client writes to the connection
        self.to_server.append(frame)  # => one direction

    def server_echo(self) -> None:  # => co-33: the server reads a frame and echoes it back over the SAME connection
        if self.to_server:  # => a frame is waiting
            frame = self.to_server.popleft()  # => read the client's frame
            self.to_client.append(Frame(payload=frame.payload))  # => co-33: echo back the OTHER direction

    def client_recv(self) -> Frame | None:  # => client reads the server's response
        if not self.to_client:  # => nothing echoed back yet
            return None  # => idle
        return self.to_client.popleft()  # => the echoed frame


ws = WebSocket()  # => co-33: ONE persistent, bidirectional connection
ws.client_send(Frame("ping"))  # => client -> server
ws.server_echo()  # => co-33: server echoes back over the same connection
echoed = ws.client_recv()  # => server -> client
assert echoed is not None  # => type-narrow
print("client sent:    'ping'")  # => Output: the sent frame
print(f"server echoed:  {echoed.payload!r}")  # => Output: the echoed frame (bidirectional round-trip)

assert echoed.payload == "ping"  # => co-33: a bidirectional round-trip over one connection
