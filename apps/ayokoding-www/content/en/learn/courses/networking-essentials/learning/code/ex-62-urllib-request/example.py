"""Example 62: urllib.request -- an Even Higher-Level HTTP Client."""

import urllib.request  # => co-23: higher-level than http.client -- takes a full URL, not host+path

URL = "http://info.cern.ch/"  # => co-02: urllib.request parses scheme/host/path FROM this string


def fetch(url: str) -> tuple[int, bytes]:  # => returns (status code, response body)
    with urllib.request.urlopen(url, timeout=5) as response:  # => co-02: parses the URL, connects  # fmt: skip
        # => and issues the request in ONE call -- no separate HTTPConnection object needed
        status = response.status  # => co-13: the numeric status code
        body = response.read()  # => the full response body, already assembled
        return status, body


status, body = fetch(URL)  # => a real GET against a real URL, via urlopen()'s one-call API  # fmt: skip
print(f"status: {status}")  # => expect 200, since URL genuinely answers
print(f"body starts with: {body[:30]!r}")  # => confirms real HTML bytes, not an empty response  # fmt: skip

assert status == 200  # => confirms urlopen() parsed a real 200 response
assert body.startswith(b"<html>")  # => confirms the body was read via response.read()
print("ex-62 OK")  # => confirms both the status parsing and the body reading round-tripped  # fmt: skip
