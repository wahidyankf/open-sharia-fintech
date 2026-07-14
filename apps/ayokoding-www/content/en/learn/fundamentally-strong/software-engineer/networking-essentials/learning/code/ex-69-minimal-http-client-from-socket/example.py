"""Example 69: A Minimal HTTP Client Built Directly on a Socket."""

import socket  # => stdlib sockets -- the ONLY import this whole HTTP client needs


def http_get_status_line(host: str, port: int, path: str) -> str:  # => DNS+TCP+HTTP, all by hand  # fmt: skip
    # co-10/co-12/co-13: every layer this topic covered, composed by hand, one more time --
    # no http.client, no urllib -- just socket.connect + a hand-written request + a raw parse.
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"  # => co-12: by hand
    with socket.create_connection((host, port), timeout=5) as sock:  # => co-07: TCP handshake  # fmt: skip
        sock.sendall(request.encode("ascii"))  # => co-12: the hand-built request, sent raw  # fmt: skip
        response = b""  # => accumulates the full response -- its final size isn't known in advance
        while True:  # => co-11: keep reading until the server closes (Connection: close)  # fmt: skip
            chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
            if not chunk:  # => an empty recv() means the server closed its side
                break
            response += chunk  # => appends this chunk -- the loop above may run several times  # fmt: skip
    status_line = response.split(b"\r\n", 1)[0].decode()  # => co-13: the FIRST line, only  # fmt: skip
    return status_line  # => the ONE value this function hands back, the whole point of calling it


status_line = http_get_status_line("example.com", 80, "/")  # => resolves, connects, requests, parses  # fmt: skip
print(f"status line: {status_line}")  # => expect a real status line, e.g. "HTTP/1.1 200 OK"  # fmt: skip

assert status_line == "HTTP/1.1 200 OK"  # => a real status line, from a real server, real bytes  # fmt: skip
print("ex-69 OK")  # => confirms a hand-built HTTP client, with zero libraries, genuinely worked  # fmt: skip
