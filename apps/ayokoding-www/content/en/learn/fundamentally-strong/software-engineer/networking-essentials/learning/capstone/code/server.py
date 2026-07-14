"""Capstone: line-based TCP command server -- PING/PONG, TIME, graceful multi-client handling.

Combines every socket mechanism this topic taught into one runnable program: bind/listen/
accept (co-10), a three-way-handshake TCP connection per client (co-07), newline-delimited
request/response framing that reassembles partial reads (co-11), a small command protocol
(co-01), SO_REUSEADDR so repeated runs never collide on a leftover TIME_WAIT socket (co-10),
one thread per connected client so multiple clients are served concurrently (co-10, co-01),
and a graceful-close detection loop that ends cleanly the instant a client disconnects (co-07).
"""

from __future__ import annotations

import argparse
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 50100  # => an ephemeral port distinct from every worked example's port (co-05)


def read_line(sock: socket.socket, buffer: bytearray) -> bytes | None:
    """Read one newline-delimited line from ``sock``, buffering partial reads across calls.

    Returns the line (without the trailing newline) once a full line has arrived, or
    ``None`` if the peer closed its side before sending one -- co-07/co-11.
    """
    while b"\n" not in buffer:  # => keep reading until a full line has actually arrived
        chunk = sock.recv(256)  # => a single recv() may return only PART of a line
        if not chunk:  # => an empty recv() means the peer closed -- co-07's graceful signal  # fmt: skip
            return None
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one line, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the NEXT call  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


def handle_command(command: bytes) -> bytes:
    """Map one command line to its reply -- co-01: the server, not the client, decides validity."""
    if command == b"PING":  # => the simplest possible liveness check
        return b"PONG"
    if command == b"TIME":  # => a command that returns SERVER-side state, not an echo
        return str(int(time.time())).encode()  # => Unix epoch seconds, as ASCII digits
    return b"ERR unknown command: " + command  # => a graceful reply, never a crash (co-11)  # fmt: skip


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """Serve one client's full session: read/reply until it disconnects, then close cleanly."""
    with conn:
        buffer = bytearray()  # => this connection's own leftover-bytes buffer (co-11)
        while True:  # => co-07: loops until the CONNECTION itself signals it is finished  # fmt: skip
            command = read_line(conn, buffer)
            if command is None:  # => co-07: the client closed -- exit this loop gracefully  # fmt: skip
                break
            reply = handle_command(command)
            conn.sendall(reply + b"\n")
    print(f"connection from {addr} closed gracefully")


def run_server(host: str, port: int, client_count: int | None) -> None:
    """Bind, listen, and serve clients on their own threads until ``client_count`` have been
    served (or forever, if ``client_count`` is ``None``) -- co-10.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # SO_REUSEADDR: an immediate restart can reuse a port stuck in TIME_WAIT (co-10).
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))  # => claims (host, port) for this process
        sock.listen(5)  # => a backlog of 5 pending, not-yet-accepted connections
        print(f"listening on {host}:{port}", flush=True)  # => the signal client.py waits for  # fmt: skip

        handlers: list[threading.Thread] = []
        served = 0
        while client_count is None or served < client_count:
            conn, addr = sock.accept()  # => co-07: blocks for the next client's handshake  # fmt: skip
            handler = threading.Thread(target=handle_client, args=(conn, addr))
            handler.start()  # => co-10: each client is served concurrently, on its own thread  # fmt: skip
            handlers.append(handler)
            served += 1
        for handler in handlers:
            handler.join()  # => waits for every spawned handler thread to finish


def main() -> None:
    parser = argparse.ArgumentParser(description="Line-based TCP command server.")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument(
        "--clients",
        type=int,
        default=None,
        help="serve exactly this many clients, then exit (default: run forever)",
    )
    args = parser.parse_args()
    run_server(args.host, args.port, args.clients)


if __name__ == "__main__":
    main()
