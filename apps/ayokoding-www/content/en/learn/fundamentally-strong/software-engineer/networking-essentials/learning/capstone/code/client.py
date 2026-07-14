"""Capstone: line-based TCP command client -- sends PING and TIME, then shuts down gracefully."""

from __future__ import annotations

import argparse
import socket

HOST = "127.0.0.1"
PORT = 50100  # => must match server.py's bound port exactly (co-05)


def read_line(sock: socket.socket, buffer: bytearray) -> bytes | None:
    """The identical framing helper server.py uses -- co-11: both sides agree on the framing."""
    while b"\n" not in buffer:
        chunk = sock.recv(256)
        if not chunk:
            return None
        buffer.extend(chunk)
    line, _, rest = buffer.partition(b"\n")
    buffer[:] = rest
    return bytes(line)


def run_client(host: str, port: int, commands: list[bytes]) -> list[bytes]:
    """Connect once, send every command in ``commands`` in order, and return every reply."""
    replies: list[bytes] = []
    with socket.create_connection((host, port), timeout=5) as sock:  # => co-07: the TCP handshake  # fmt: skip
        buffer = bytearray()
        for command in commands:  # => co-11: many messages, ONE persistent connection
            sock.sendall(command + b"\n")
            reply = read_line(sock, buffer)
            if reply is None:  # => the server closed unexpectedly -- surfaced, not swallowed  # fmt: skip
                raise ConnectionError("server closed before replying")
            replies.append(reply)
        # Exiting this `with` block calls close() -- co-07: this IS the graceful shutdown
        # server.py's read_line() detects as an empty recv() and handles cleanly.
    return replies


def main() -> None:
    parser = argparse.ArgumentParser(description="Line-based TCP command client.")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()

    replies = run_client(args.host, args.port, [b"PING", b"TIME"])
    print(f"PING -> {replies[0]!r}")
    print(f"TIME -> {replies[1]!r}")

    assert replies[0] == b"PONG"  # => confirms the fixed-response command
    assert replies[1].isdigit()  # => confirms TIME returned a plausible epoch timestamp
    print("capstone client OK")


if __name__ == "__main__":
    main()
