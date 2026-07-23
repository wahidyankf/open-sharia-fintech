"""Example 71: Two Requests, One Keep-Alive Connection."""

import http.client  # => co-23: the same stdlib client -- keep-alive is a property of ONE conn

HOST = "info.cern.ch"  # => a plain, non-chunked host -- keeps this example's output simple  # fmt: skip

# HTTP/1.1 defaults to keep-alive: the SAME TCP connection can carry MULTIPLE requests,
# avoiding a fresh handshake (co-07) for every single one (co-12).
conn = http.client.HTTPConnection(HOST, 80, timeout=5)  # => ONE connection object

conn.request("GET", "/")  # => request 1, over the connection
first = conn.getresponse()  # => co-13: parses request 1's status line + headers
first_status = first.status  # => captured BEFORE request 2 reuses the same conn object
first.read()  # => MUST fully read the body before reusing the connection for request 2

conn.request("GET", "/")  # => request 2, over the EXACT SAME socket -- no reconnect happened  # fmt: skip
second = conn.getresponse()  # => co-13: parses request 2's status line + headers
second_status = second.status  # => captured from the SAME conn, no new HTTPConnection() call  # fmt: skip
second.read()  # => drains request 2's body before the connection finally closes below

conn.close()  # => only NOW does the underlying socket actually close

print(f"request 1 status: {first_status}")
print(f"request 2 status: {second_status}")

assert first_status == 200  # => confirms both requests succeeded ...
assert second_status == 200  # => ... over what was, underneath, a single TCP connection
print("ex-71 OK")  # => confirms two full request/response cycles shared one real connection  # fmt: skip
