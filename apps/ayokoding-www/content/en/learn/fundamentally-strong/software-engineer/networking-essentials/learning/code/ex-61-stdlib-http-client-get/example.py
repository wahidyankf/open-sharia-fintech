"""Example 61: http.client -- a GET Request via the Standard Library."""

import http.client  # => co-23: a stdlib HTTP client, no raw sockets and no third-party package

HOST = "info.cern.ch"  # => a plain, non-chunked host -- keeps this example's output simple  # fmt: skip


def fetch(host: str, path: str) -> tuple[int, bytes]:  # => returns (status code, response body)  # fmt: skip
    conn = http.client.HTTPConnection(host, 80, timeout=5)  # => co-23: builds ON the socket API  # fmt: skip
    try:  # => wrapped so conn.close() below always runs, even if request()/getresponse() raises
        conn.request("GET", path)  # => co-14: sends a GET -- http.client writes the request line  # fmt: skip
        # => and headers for you, but it is still the exact request line/headers shape (co-12)
        # Example 43 hand-crafted over a raw socket
        response = conn.getresponse()  # => co-13: parses the status line + headers automatically  # fmt: skip
        status = response.status  # => an int, e.g. 200 -- no manual string-splitting needed  # fmt: skip
        body = response.read()  # => reads (and, if needed, de-chunks) the full body for you  # fmt: skip
        return status, body
    finally:
        conn.close()  # => releases the underlying socket


status, body = fetch(HOST, "/")  # => a real GET against a real host, via the stdlib client  # fmt: skip
print(f"status: {status}")  # => expect 200, since HOST genuinely answers
print(f"body starts with: {body[:30]!r}")  # => confirms real HTML bytes, not an empty response  # fmt: skip

assert status == 200  # => confirms the stdlib client parsed a real 200 response
assert body.startswith(b"<html>")  # => confirms the body was read (and any chunking undone)  # fmt: skip
print("ex-61 OK")  # => confirms both the status parsing and the body reading round-tripped  # fmt: skip
