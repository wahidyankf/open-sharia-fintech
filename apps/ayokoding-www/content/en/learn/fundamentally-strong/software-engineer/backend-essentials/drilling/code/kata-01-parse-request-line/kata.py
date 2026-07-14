def parse_request_line(line: str) -> tuple[str, str, str]:  # => co-01: request = method + path + version
    parts = line.strip().split(" ")  # => splits "GET /items/5 HTTP/1.1" into 3 whitespace-separated fields
    if len(parts) != 3:  # => a well-formed request line always has exactly 3 space-separated tokens
        raise ValueError(f"malformed request line: {line!r}")  # => not a shape a server should ever accept
    method, path, version = parts  # => unpack in RFC 9110's canonical order: method, target, version
    return method, path, version  # => the caller gets the three parts a handler dispatches on


line = "GET /items/5 HTTP/1.1"  # => a mocked raw request line, never touching a socket
method, path, version = parse_request_line(line)
print(method, path, version)  # => Output: GET /items/5 HTTP/1.1

assert method == "GET"  # => the verb that carries "read" semantics (co-02)
assert path == "/items/5"  # => the resource being addressed, with a path param baked in (co-12)
assert version == "HTTP/1.1"

try:
    parse_request_line("not a valid line")  # => only 3 tokens are required; this has 4
    raised = False
except ValueError:  # => malformed input is rejected loudly, not silently mis-parsed
    raised = True
print(raised)  # => Output: True

assert raised is True
print("kata-01 OK")
