"""Example 59: connect() to an Open Port vs. a Closed Port."""

import socket  # => stdlib sockets -- connect() itself is the whole demonstration here

OPEN_HOST = "example.com"  # => co-05: a real host with a real listener on port 443 (HTTPS)  # fmt: skip
OPEN_PORT = 443  # => HTTPS's well-known port -- genuinely has something listening
CLOSED_HOST = "127.0.0.1"  # => loopback -- guaranteed nothing is listening on this port
CLOSED_PORT = 50059  # => deliberately unused in this entire topic's port range


def try_connect(host: str, port: int) -> str:  # => co-10: connect() either succeeds or raises  # fmt: skip
    try:  # => wrapped so a refused connection doesn't crash the script -- it raises instead
        with socket.create_connection((host, port), timeout=5):  # => the actual connect() attempt  # fmt: skip
            return "connected successfully"  # => reached only if the handshake truly completed
    except ConnectionRefusedError as err:  # => co-10: the OS actively rejected the SYN
        return f"ConnectionRefusedError: {err}"  # => the exact exception text, so both cases print


open_result = try_connect(OPEN_HOST, OPEN_PORT)  # => a genuinely open, real remote port
closed_result = try_connect(CLOSED_HOST, CLOSED_PORT)  # => a genuinely closed local port  # fmt: skip

print(f"{OPEN_HOST}:{OPEN_PORT} -> {open_result}")  # => expect "connected successfully"
print(f"{CLOSED_HOST}:{CLOSED_PORT} -> {closed_result}")  # => expect "ConnectionRefusedError: ..."  # fmt: skip

assert open_result == "connected successfully"  # => confirms the genuinely open port succeeds  # fmt: skip
assert closed_result.startswith("ConnectionRefusedError")  # => confirms the closed port raises, not hangs  # fmt: skip
print("ex-59 OK")  # => confirms both the success case and the failure case were reproduced  # fmt: skip
