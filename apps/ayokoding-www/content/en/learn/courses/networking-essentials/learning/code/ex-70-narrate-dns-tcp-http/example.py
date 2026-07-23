"""Example 70: Narrate DNS -> TCP -> HTTP for a Real Request."""

import socket  # => stdlib sockets -- both the DNS and TCP stages below live in this one module
import time  # => perf_counter() is what turns each stage into a real, comparable number

HOST = "example.com"  # => co-01: the same demo host resolved throughout this topic
PORT = 80  # => co-05: HTTP's well-known port
PATH = "/"  # => co-02: the simplest possible request path


def narrate(host: str, port: int, path: str) -> None:  # => prints one line per stage as it happens  # fmt: skip
    # Stage 1 -- DNS: name -> address (co-03). Nothing below this line can happen without it.
    dns_start = time.perf_counter()  # => a clock reading taken right before the DNS lookup  # fmt: skip
    address = socket.gethostbyname(host)  # => a real, blocking resolver call
    dns_ms = (time.perf_counter() - dns_start) * 1000  # => convert seconds to milliseconds  # fmt: skip
    print(f"[DNS]  {host} -> {address}  ({dns_ms:.1f} ms)")  # => stage 1's own isolated timing  # fmt: skip

    # Stage 2 -- TCP: address -> an open, reliable byte-stream connection (co-07).
    tcp_start = time.perf_counter()  # => a SEPARATE clock, so DNS time isn't folded into this  # fmt: skip
    sock = socket.create_connection((address, port), timeout=5)  # => the three-way handshake  # fmt: skip
    tcp_ms = (time.perf_counter() - tcp_start) * 1000  # => convert seconds to milliseconds  # fmt: skip
    print(f"[TCP]  connected to {address}:{port}  ({tcp_ms:.1f} ms)")  # => stage 2's own timing  # fmt: skip

    # Stage 3 -- HTTP: a request/response message exchanged OVER that open connection (co-12).
    http_start = time.perf_counter()  # => a THIRD clock, isolating just the request/response  # fmt: skip
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"  # => co-12: by hand
    sock.sendall(request.encode("ascii"))  # => co-12: the hand-built request, sent as raw bytes  # fmt: skip
    response = b""  # => accumulates the full response -- its final size isn't known in advance  # fmt: skip
    while True:  # => co-11: loop until the server closes (Connection: close makes this safe)  # fmt: skip
        chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
        if not chunk:  # => an empty recv() means the server closed its side
            break
        response += chunk  # => appends this chunk -- the loop above may run several times  # fmt: skip
    sock.close()  # => releases the socket once the full response has been read
    http_ms = (time.perf_counter() - http_start) * 1000  # => convert seconds to milliseconds  # fmt: skip
    status_line = response.split(b"\r\n", 1)[0].decode()  # => co-13: the FIRST line, only  # fmt: skip
    print(f"[HTTP] {status_line}  ({http_ms:.1f} ms)")  # => stage 3's own isolated timing  # fmt: skip


narrate(HOST, PORT, PATH)  # => runs all three stages, timing each one separately, in sequence  # fmt: skip
print("ex-70 OK -- three distinct layers, three distinct stages, one real request")
