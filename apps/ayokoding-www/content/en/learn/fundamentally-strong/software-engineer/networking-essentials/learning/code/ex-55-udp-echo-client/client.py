"""Example 55: UDP Echo Client."""

import socket  # => stdlib sockets -- SOCK_DGRAM below is the only difference from TCP clients

HOST = "127.0.0.1"  # => loopback -- must match Example 54's server address exactly
PORT = 50054  # => must match the server's bound port exactly


def run_client(message: bytes) -> bytes:  # => sends ONE datagram, reads ONE datagram back  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # => no connect() call at all  # fmt: skip
        sock.settimeout(5)  # => co-08: UDP has no delivery guarantee -- a timeout avoids hanging  # fmt: skip
        sock.sendto(message, (HOST, PORT))  # => fires the datagram -- no handshake, no ack  # fmt: skip
        reply, _ = sock.recvfrom(1024)  # => blocks until a reply arrives, or the timeout fires  # fmt: skip
        return reply  # => the sender's own address (the second tuple item) is discarded here


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    reply = run_client(b"hello over udp")  # => Example 54's server must already be running  # fmt: skip
    print(f"client received: {reply!r}")  # => confirms the echoed bytes match what was sent  # fmt: skip
    assert reply == b"hello over udp"  # => confirms this ONE datagram made the full round trip  # fmt: skip
    print("ex-55 OK")  # => confirms the connectionless round trip completed without a handshake  # fmt: skip
