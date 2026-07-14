"""Capstone: resolve a real host, open a TCP socket, issue a GET, narrate DNS -> TCP -> HTTP.

Ties together every layer this topic covered, in the order a real request actually
travels: DNS resolution (co-03), a TCP three-way handshake (co-07), and an HTTP
request/response exchanged over that connection (co-12, co-13) -- with a UDP contrast
note (co-08, co-09) explaining, in prose, how this same journey would differ over UDP.
"""

from __future__ import annotations

import argparse
import socket
import time


def resolve(host: str) -> str:
    """Stage 1 -- DNS: translate a hostname to an IPv4 address (co-03)."""
    start = time.perf_counter()
    address = socket.gethostbyname(host)  # => a real, blocking resolver call
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"[DNS]  {host} -> {address}  ({elapsed_ms:.1f} ms)")
    return address


def open_tcp_connection(address: str, port: int) -> socket.socket:
    """Stage 2 -- TCP: open a reliable, ordered byte-stream connection (co-07)."""
    start = time.perf_counter()
    sock = socket.create_connection((address, port), timeout=5)  # => the three-way handshake  # fmt: skip
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"[TCP]  connected to {address}:{port}  ({elapsed_ms:.1f} ms)")
    return sock


def issue_get(sock: socket.socket, host: str, path: str) -> str:
    """Stage 3 -- HTTP: send a hand-crafted GET and return the response's status line (co-12)."""
    start = time.perf_counter()
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    sock.sendall(request.encode("ascii"))
    response = b""
    while True:  # => co-11: loop until the server closes (Connection: close makes this safe)  # fmt: skip
        chunk = sock.recv(4096)
        if not chunk:
            break
        response += chunk
    sock.close()
    elapsed_ms = (time.perf_counter() - start) * 1000
    status_line = response.split(b"\r\n", 1)[0].decode()
    print(f"[HTTP] {status_line}  ({elapsed_ms:.1f} ms)")
    return status_line


def print_udp_contrast() -> None:
    """A prose note contrasting this TCP/HTTP journey with the same journey over UDP (co-08, co-09)."""
    print("[UDP contrast]")
    print(
        "  The DNS lookup in Stage 1 itself almost certainly traveled over UDP: a single,"
        " connectionless query datagram out, a single response datagram back, no handshake"
        " at all -- exactly co-08's 'no delivery guarantee' definition. If that datagram had"
        " been dropped, gethostbyname() would simply have retried or raised an error; there"
        " is no equivalent of TCP's SYN/SYN-ACK/ACK to renegotiate. Stages 2 and 3 above, by"
        " contrast, ran over TCP: one handshake, then a RELIABLE, ORDERED byte stream --"
        " which is exactly why HTTP (a byte-stream-oriented, framed protocol, co-11) is built"
        " on TCP rather than UDP: HTTP needs the ordering and delivery guarantee UDP does not"
        " provide (co-09)."
    )


def explore(host: str, port: int, path: str) -> str:
    """Run all three stages against a real host and return the final status line."""
    print(f"=== exploring {host}{path} ===")
    address = resolve(host)
    sock = open_tcp_connection(address, port)
    status_line = issue_get(sock, host, path)
    print_udp_contrast()
    return status_line


def main() -> None:
    parser = argparse.ArgumentParser(description="Narrate DNS -> TCP -> HTTP for a real host.")  # fmt: skip
    parser.add_argument("--host", default="example.com")
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--path", default="/")
    args = parser.parse_args()

    status_line: str = explore(args.host, args.port, args.path)
    assert status_line.startswith("HTTP/1.1 200")  # => confirms a real, successful response  # fmt: skip
    print("explore.py OK")


if __name__ == "__main__":
    main()
