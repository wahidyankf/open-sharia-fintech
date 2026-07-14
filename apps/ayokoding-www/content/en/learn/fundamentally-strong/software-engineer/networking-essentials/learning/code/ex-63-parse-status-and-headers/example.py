"""Example 63: Reading resp.status and resp.getheaders() Directly."""

import http.client  # => co-23: the same lower-level client Example 61 used, no urllib this time

conn = http.client.HTTPConnection("info.cern.ch", 80, timeout=5)  # => co-23: same triple as Ex 61  # fmt: skip
conn.request("GET", "/")  # => co-14: sends the GET -- no response has been read yet
response = conn.getresponse()  # => co-13: parses the status line + headers, body still unread  # fmt: skip

status = response.status  # => co-13/co-23: the status code as a plain int, e.g. 200
reason = response.reason  # => co-13: the human-readable reason phrase, e.g. "OK"
headers = response.getheaders()  # => co-16/co-23: a list of (name, value) tuples, in order  # fmt: skip
body = response.read()  # => reads the body LAST -- headers are already fully parsed by now  # fmt: skip
conn.close()  # => releases the underlying socket once every value needed has been captured

print(f"status: {status} {reason}")  # => the int status paired with its human-readable reason  # fmt: skip
print(f"header count: {len(headers)}")  # => how many (name, value) pairs getheaders() found  # fmt: skip
for name, value in headers:  # => co-16: every header the raw response carried, already parsed  # fmt: skip
    print(f"  {name}: {value}")  # => each header printed on its own line, name and value split  # fmt: skip

header_names = {name.lower() for name, _ in headers}  # => co-08: a set for O(1) membership checks  # fmt: skip
assert status == 200  # => confirms the request itself genuinely succeeded
assert "content-length" in header_names  # => confirms a specific header was actually parsed out  # fmt: skip
declared_length = int(response.getheader("Content-Length", "0"))  # => the header's CLAIMED size  # fmt: skip
assert declared_length == len(body)  # => co-16/co-13: header value matches the real body size  # fmt: skip
print("ex-63 OK")  # => confirms status, headers, and the Content-Length cross-check all held  # fmt: skip
