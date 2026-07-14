"""Example 68: Read a 301/302 Location Header, Then Request It Manually."""

import http.client  # => co-23: the same stdlib client Examples 61/63/64 used
from urllib.parse import urlsplit  # => co-02: the SAME URL parser Example 7 introduced

HOST = "go.dev"  # => a real host that redirects plain HTTP to HTTPS (co-18)


# Step 1: request the ORIGINAL, plaintext URL -- expect a redirect, not the final page.
conn = http.client.HTTPConnection(HOST, 80, timeout=5)  # => co-23: plaintext port -- same as Ex 61  # fmt: skip
conn.request("GET", "/")  # => co-14: the FIRST of two requests this example makes
first_response = conn.getresponse()  # => co-13: parses the redirect status line + headers  # fmt: skip
first_status = first_response.status  # => co-15: a 3xx status signals "go elsewhere instead"  # fmt: skip
location = first_response.getheader("Location")  # => co-18: WHERE to go instead
first_response.read()  # => drains the (usually empty) redirect body before closing
conn.close()  # => releases the FIRST connection -- the second request needs its own connection

print(f"first request: {first_status}, Location: {location}")  # => co-15: a 3xx, plus WHERE to go  # fmt: skip

assert location is not None  # => confirms a Location header was actually present
assert first_status in (301, 302, 307, 308)  # => confirms this really was a redirect status  # fmt: skip

# Step 2: parse the Location header and issue a SECOND, manual request to it (co-18).
parsed = urlsplit(location)  # => co-02: breaks the redirect target into scheme/host/path parts  # fmt: skip
assert parsed.hostname is not None  # => narrows str | None to str for the type checker
target_host: str = parsed.hostname  # => the SECOND request's host -- may differ from HOST above  # fmt: skip
follow_conn: http.client.HTTPConnection  # => declared here since its concrete type varies below  # fmt: skip
if parsed.scheme == "https":  # => co-17: the redirect target may switch schemes entirely  # fmt: skip
    follow_conn = http.client.HTTPSConnection(target_host, timeout=5)  # => co-17: TLS this time  # fmt: skip
else:
    follow_conn = http.client.HTTPConnection(target_host, timeout=5)  # => stays plaintext  # fmt: skip
follow_conn.request("GET", parsed.path or "/")  # => co-14: the SECOND request, to the NEW target  # fmt: skip
final_response = follow_conn.getresponse()  # => co-13: parses the FINAL page's status + headers  # fmt: skip
final_status = final_response.status  # => expected to be a real 200, not another redirect  # fmt: skip
final_response.read()  # => drains the final page's body before closing
follow_conn.close()  # => releases the SECOND connection

print(f"second request (to {location}): {final_status}")

assert final_status == 200  # => confirms manually following the redirect reached the real page  # fmt: skip
print("ex-68 OK")  # => confirms both the redirect detection and the manual follow-up succeeded  # fmt: skip
