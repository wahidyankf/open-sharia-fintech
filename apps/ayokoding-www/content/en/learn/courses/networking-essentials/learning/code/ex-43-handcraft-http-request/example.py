"""Example 43: Handcraft an HTTP Request Over a Raw Socket."""

import socket  # => stdlib sockets -- no HTTP library imported anywhere in this file

HOST = "example.com"  # => a real, RFC-2606-reserved documentation host (co-01)
PORT = 80  # => co-05: HTTP's well-known port

# co-12: an HTTP/1.1 request is a request line, headers, then a BLANK line -- \r\n\r\n.
# There is no HTTP library involved anywhere here -- these are the literal bytes on the wire.
request = (  # => plain string concatenation -- no HTTP library builds this for us
    "GET / HTTP/1.1\r\n"  # => the request line: METHOD, PATH, VERSION
    "Host: example.com\r\n"  # => co-16: HTTP/1.1 REQUIRES a Host header (one server, many sites)
    "Connection: close\r\n"  # => tells the server to close after replying, simplifying this demo
    "\r\n"  # => the blank line that ends the headers -- REQUIRED even with no body
)

with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => co-07: the TCP handshake  # fmt: skip
    sock.sendall(request.encode("ascii"))  # => co-12: HTTP headers are ASCII, sent as raw bytes  # fmt: skip
    response = b""  # => accumulates the full response -- its final size isn't known in advance  # fmt: skip
    while True:  # => co-11: loop until the server closes (Connection: close makes this safe)  # fmt: skip
        chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
        if not chunk:  # => an empty recv() means the server closed its side
            break
        response += chunk  # => appends this chunk -- the loop above may run several times  # fmt: skip

status_line = response.split(b"\r\n", 1)[0]  # => co-13: everything up to the first \r\n
print(f"status line: {status_line.decode()}")  # => decoded to str only for display purposes  # fmt: skip

assert status_line == b"HTTP/1.1 200 OK"  # => confirms a hand-crafted request gets a real reply  # fmt: skip
print("ex-43 OK")  # => confirms the request/response round trip completed with the expected status  # fmt: skip
