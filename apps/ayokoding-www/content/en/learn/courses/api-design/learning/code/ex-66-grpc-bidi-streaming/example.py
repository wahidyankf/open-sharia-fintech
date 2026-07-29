# pyright: strict
"""Example 66: A Bidirectional-Streaming RPC. (co-26)

Bidirectional streaming lets BOTH sides send a sequence of messages over
the SAME call, interleaved -- unlike Example 65's server-only stream, here
the client streams requests in while simultaneously reading responses out,
modeled here as an interleaved read/write loop over a shared connection.
"""

from collections.abc import Iterator  # => co-26: both the input and output are streams
from dataclasses import dataclass  # => typed request/response messages


@dataclass  # => co-26: ONE message the client streams IN, per chat line
class ChatMessage:
    text: str  # => the message text this participant sent


def echo_uppercase_bidi(client_stream: Iterator[ChatMessage]) -> Iterator[ChatMessage]:  # => co-26: bidi RPC
    for incoming in client_stream:  # => co-26: reads ONE client message at a time, as it arrives
        reply = ChatMessage(text=incoming.text.upper())  # => co-26: the server's own per-message reply
        yield reply  # => co-26: streams the reply back IMMEDIATELY -- interleaved, not batched at the end


def client_messages() -> Iterator[ChatMessage]:  # => co-26: simulates the client's OWN outbound stream
    yield ChatMessage(text="hello")  # => client message 1
    yield ChatMessage(text="from")  # => client message 2
    yield ChatMessage(text="grpc")  # => client message 3


interleaved_pairs: list[tuple[str, str]] = []  # => co-26: records (sent, received) pairs, in arrival order
server_replies = echo_uppercase_bidi(client_messages())  # => co-26: wires the client stream INTO the server
for sent, received in zip(client_messages(), server_replies, strict=True):  # => co-26: walks both streams
    interleaved_pairs.append((sent.text, received.text))  # => co-26: pairs each send with its own reply

for sent_text, received_text in interleaved_pairs:  # => print each interleaved exchange
    print(f"sent={sent_text!r} -> received={received_text!r}")  # => Output: 3 lines, each upper-cased
# => neither side waited for the OTHER's entire stream to finish before replying
