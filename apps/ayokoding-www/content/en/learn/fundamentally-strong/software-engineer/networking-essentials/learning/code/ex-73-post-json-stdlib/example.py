"""Example 73: POST JSON with http.client, Explicit Content-Type Header."""

import http.client  # => co-23: the same stdlib client, this time issuing a POST, not a GET
import json  # => co-14: encodes the Python dict below into the wire-format JSON body

HOST = "postman-echo.com"  # => echoes back exactly what it received, ideal for verification

payload = {"event": "networking-essentials", "example": 73}  # => co-22: a typed dict literal  # fmt: skip
body = json.dumps(payload).encode("utf-8")  # => co-14: JSON text, encoded to raw bytes

conn = http.client.HTTPSConnection(HOST, 443, timeout=5)  # => co-23: HTTPS, like Example 72  # fmt: skip
conn.request(  # => co-14: unlike GET, POST carries a body AND needs matching headers
    "POST",  # => co-14: POST -- creating/submitting data, unlike GET's read-only semantics
    "/post",  # => postman-echo's dedicated POST-echoing endpoint
    body=body,  # => the JSON bytes built above -- http.client sends these as the request body
    headers={  # => co-16: headers the SERVER needs to correctly interpret the body
        "Content-Type": "application/json",  # => tells the server HOW to parse the body
        # => tells the server exactly how many bytes to read
        "Content-Length": str(len(body)),
    },  # => end of the headers dict
)  # => end of the request() call -- the POST has now genuinely gone out
response = conn.getresponse()  # => co-13: parses the echoed response's status line + headers  # fmt: skip
status = response.status  # => an int, e.g. 200 -- the POST's own success/failure signal
response_body = json.loads(response.read())  # => postman-echo replies with JSON describing what it saw  # fmt: skip
conn.close()  # => releases the connection once the echoed body has been fully read and parsed

print(f"status: {status}")  # => expect 200, since the POST itself genuinely succeeded
print(f"echoed content-type: {response_body['headers']['content-type']}")  # => the header round-trip  # fmt: skip
print(f"echoed json: {response_body['json']}")  # => the exact payload dict, echoed back unchanged  # fmt: skip

assert status == 200  # => confirms the POST itself succeeded
assert response_body["headers"]["content-type"] == "application/json"  # => header arrived intact  # fmt: skip
assert response_body["json"] == payload  # => confirms the exact payload round-tripped correctly  # fmt: skip
print("ex-73 OK")  # => confirms the headers, encoding, and body all worked together correctly  # fmt: skip
