"""Example 44: Split a Raw HTTP Response into Status Line, Headers, and Body."""

import socket  # => stdlib sockets -- fetch_raw below is the SAME pattern as Example 43

# info.cern.ch (the first website ever put online) replies with a plain, fixed-length
# body -- example.com's CDN replies chunked instead, which would mix chunk-size framing
# into "the body" and distract from this example's actual point (co-13: splitting a
# message into status line + headers + body). Example 53 covers chunked bodies directly.
HOST = "info.cern.ch"  # => chosen SPECIFICALLY for its plain, non-chunked response shape  # fmt: skip
PORT = 80  # => co-05: HTTP's well-known port


def fetch_raw(host: str, port: int, path: str) -> bytes:  # => same handcrafted request as Ex 43  # fmt: skip
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    with socket.create_connection((host, port), timeout=5) as sock:  # => co-07: the TCP handshake  # fmt: skip
        sock.sendall(request.encode("ascii"))  # => co-12: the raw request bytes, sent as-is  # fmt: skip
        response = b""  # => accumulates the full response -- its final size isn't known upfront
        while True:  # => co-11: loop until the server closes (Connection: close makes this safe)  # fmt: skip
            chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
            if not chunk:  # => an empty recv() means the server closed its side
                break
            response += chunk  # => appends this chunk -- the loop above may run several times  # fmt: skip
    return response  # => the FULL raw response: status line + headers + blank line + body, as bytes


raw = fetch_raw(HOST, PORT, "/")  # => one function call replaces Example 43's inline socket code  # fmt: skip

# co-13: the blank line \r\n\r\n is the ONE fixed boundary every HTTP/1.1 message has --
# everything before it is the status line + headers; everything after it is the body.
head, _, body = raw.partition(b"\r\n\r\n")  # => splits into exactly TWO parts at the first match  # fmt: skip
lines = head.split(b"\r\n")  # => the headers block splits cleanly on individual \r\n boundaries  # fmt: skip
status_line = lines[0]  # => co-13: version + code + reason, e.g. "HTTP/1.1 200 OK"
header_lines = lines[1:]  # => every remaining line before the blank line is one header

print(f"status line: {status_line.decode()}")
print(f"header count: {len(header_lines)}")
print(f"first header: {header_lines[0].decode()}")
print(f"body starts with: {body[:40]!r}")

assert status_line.startswith(b"HTTP/1.1 200")  # => confirms the status-line split is correct  # fmt: skip
assert len(header_lines) > 0  # => confirms at least one header was isolated
assert body.startswith(b"<html>")  # => confirms the body split lands on real HTML, not headers  # fmt: skip
print("ex-44 OK")  # => confirms the three-way split (status/headers/body) was correct end to end  # fmt: skip
