"""Example 67: HTTP (Plaintext) vs. HTTPS (Encrypted) -- Proven, Not Assumed."""

import socket  # => stdlib sockets -- deliberately NOT http.client, so no TLS is ever negotiated

HOST = "example.com"  # => co-01: a real host that genuinely serves both plaintext and TLS ports


def fetch_plaintext_over(port: int) -> bytes:  # => sends the SAME raw bytes to either port  # fmt: skip
    request = f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n".encode()
    with socket.create_connection((HOST, port), timeout=5) as sock:  # => co-05: port varies, host doesn't  # fmt: skip
        sock.sendall(request)  # => co-17: no TLS handshake attempted here -- raw bytes only  # fmt: skip
        data = b""  # => accumulates whatever bytes come back, however the port chooses to respond
        sock.settimeout(3)  # => bounds the read loop below in case a port simply stays silent  # fmt: skip
        try:  # => port 443 may time out instead of replying -- that path is handled, not a crash
            while True:  # => co-11: loop until the peer closes or the timeout above fires  # fmt: skip
                chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes  # fmt: skip
                if not chunk:  # => an empty recv() means the server closed its side
                    break
                data += chunk  # => appends this chunk -- the loop above may run several times
        except TimeoutError:  # => co-17: 443 may simply refuse to reply to un-negotiated bytes  # fmt: skip
            pass
    return data  # => whatever WAS received before close or timeout, possibly a real HTTP reply


# Port 80: plain HTTP happily reads and answers the raw request line/headers (co-01/co-12).
port_80_response = fetch_plaintext_over(80)  # => the exact same request bytes as port 443 below  # fmt: skip
port_80_status = port_80_response.split(b"\r\n", 1)[0]  # => co-13: everything up to the first \r\n  # fmt: skip
print(f"port 80 (plaintext), sent raw HTTP directly: {port_80_status.decode()}")

# Port 443: the SAME raw plaintext bytes, sent to the TLS port WITHOUT a TLS handshake.
# The server can tell these aren't a valid TLS ClientHello and rejects them -- but Cloudflare's
# edge specifically detects "this looks like plain HTTP" and replies in PLAIN TEXT to explain
# why, rather than staying silent -- proof port 443 expects encryption, not proof of silence.
port_443_response = fetch_plaintext_over(443)  # => identical request() call, different PORT only  # fmt: skip
port_443_status = port_443_response.split(b"\r\n", 1)[0]  # => co-13: the same parsing as port 80  # fmt: skip
print(f"port 443 (expects TLS), sent raw HTTP directly: {port_443_status.decode()}")

assert port_80_status == b"HTTP/1.1 200 OK"  # => co-17: port 80 speaks plain HTTP, no complaints  # fmt: skip
assert port_443_status == b"HTTP/1.1 400 Bad Request"  # => port 443 rejects un-encrypted bytes  # fmt: skip
assert b"plain HTTP request was sent to HTTPS port" in port_443_response  # => the WHY, in plain text  # fmt: skip
# co-17: a REAL TLS-negotiated request to this same port 443 (Examples 64-66) succeeds with a
# real 200 -- the difference is entirely the TLS handshake this script deliberately skipped.
print("ex-67 OK")  # => confirms both ports were probed with the identical plaintext request  # fmt: skip
