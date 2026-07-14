"""Example 72: Branch on Status Class -- 404 vs. 500, Handled Explicitly."""

import http.client  # => co-23: the same stdlib client -- mock.codes is real, live HTTPS

HOST = "mock.codes"  # => a service purpose-built to return an exact requested status code  # fmt: skip


def fetch_status(path: str) -> int:  # => the path ITSELF picks the status code mock.codes returns  # fmt: skip
    conn = http.client.HTTPSConnection(HOST, 443, timeout=5)  # => co-23: a fresh conn per call  # fmt: skip
    conn.request("GET", path)  # => co-14: e.g. GET /404 genuinely returns a 404, by design  # fmt: skip
    response = conn.getresponse()  # => co-13: parses the real status line + headers
    response.read()  # => drains the body so the connection can close cleanly
    conn.close()  # => releases this call's own connection
    return response.status  # => the ONE value this function hands back to its caller


def classify(status: int) -> str:  # => co-15: branch on the STATUS CLASS, not the exact code  # fmt: skip
    if 200 <= status < 300:  # => co-15: the 2xx class -- request succeeded
        return "success"  # => the ONLY branch with no retry consideration at all
    if 400 <= status < 500:  # => co-15: the 4xx class -- something about THIS request was wrong  # fmt: skip
        return "client error -- the REQUEST was likely wrong, retrying unchanged won't help"  # => 404 lands here
    if 500 <= status < 600:  # => co-15: the 5xx class -- the SERVER had the problem, not the client  # fmt: skip
        return "server error -- the request was probably fine, retrying LATER might help"  # => 500 lands here
    return "unhandled class"  # => co-15: any status outside 2xx/4xx/5xx this function checks for


not_found_status = fetch_status("/404")  # => a genuinely fetched 404, not a hardcoded literal  # fmt: skip
server_error_status = fetch_status("/500")  # => a genuinely fetched 500, not a hardcoded literal  # fmt: skip

print(f"/404 -> {not_found_status}: {classify(not_found_status)}")  # => the 4xx branch, live  # fmt: skip
print(f"/500 -> {server_error_status}: {classify(server_error_status)}")  # => the 5xx branch, live  # fmt: skip

assert classify(not_found_status).startswith("client error")  # => confirms the 4xx branch fired  # fmt: skip
assert classify(server_error_status).startswith("server error")  # => confirms the 5xx branch  # fmt: skip
print("ex-72 OK")  # => confirms both real status codes routed through the correct classify() branch  # fmt: skip
