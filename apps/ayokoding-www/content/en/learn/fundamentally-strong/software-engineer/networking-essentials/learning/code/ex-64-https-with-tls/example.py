"""Example 64: HTTPSConnection -- A GET Request Encrypted with TLS."""

import http.client  # => co-23: the same stdlib client -- HTTPSConnection lives right alongside it

HOST = "example.com"  # => co-01: the same demo host every dig-based example resolved

# HTTPSConnection is HTTPConnection PLUS a TLS handshake, transparently -- co-17: the same
# GET/request/getresponse API as Example 61, but every byte on the wire is now encrypted.
conn = http.client.HTTPSConnection(HOST, 443, timeout=5)  # => co-05: HTTPS's well-known port  # fmt: skip
conn.request("GET", "/")  # => co-14: sends the GET -- identical call shape to Example 61  # fmt: skip
response = conn.getresponse()  # => co-13: parses the (now decrypted) status line + headers  # fmt: skip
status = response.status  # => an int, e.g. 200 -- unchanged by TLS being present
body = response.read()  # => the decrypted body, already assembled -- no manual TLS handling  # fmt: skip
conn.close()  # => releases the underlying encrypted connection

print(f"status: {status}")  # => expect 200, since HOST genuinely answers over HTTPS
print(f"body starts with: {body[:30]!r}")  # => confirms real HTML bytes, not TLS handshake bytes  # fmt: skip

assert status == 200  # => confirms a real, successfully DECRYPTED 200 response
assert body.startswith(b"<!doctype")  # => confirms the actual HTML, not TLS handshake bytes  # fmt: skip
print("ex-64 OK")  # => confirms the same request/response cycle worked, now fully encrypted  # fmt: skip
