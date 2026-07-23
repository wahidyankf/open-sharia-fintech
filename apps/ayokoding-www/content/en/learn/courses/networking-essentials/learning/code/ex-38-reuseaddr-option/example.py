"""Example 38: SO_REUSEADDR -- Restarting a Server Without "Address Already in Use"."""

import socket  # => stdlib sockets -- SO_REUSEADDR is a setsockopt() flag, not a separate API

HOST = "127.0.0.1"  # => loopback -- keeps this TIME_WAIT demo local and deterministic
PORT = 50038  # => co-05: a fresh ephemeral port, reused deliberately three times below


def bind_serve_and_close(reuse: bool) -> socket.socket:
    # Returns a BOUND, LISTENING socket -- the caller decides when to close it, so this
    # function can demonstrate the exact moment a port becomes reusable (or doesn't).
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => a fresh IPv4 TCP socket each call  # fmt: skip
    if reuse:  # => co-10: SO_REUSEADDR lets a new socket bind to a port stuck in TIME_WAIT  # fmt: skip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))  # => this is the call that fails if the port is still TIME_WAIT'd  # fmt: skip
    sock.listen(1)  # => flips the socket passive -- required before this fn can be reused  # fmt: skip
    return sock  # => intentionally NOT closed here -- the caller controls WHEN it closes  # fmt: skip


# Step 1: bind, accept one real connection, then CLOSE THE SERVER SIDE FIRST -- an active
# close is exactly what puts this local port into TIME_WAIT (a passive close would not).
first_server = bind_serve_and_close(reuse=True)  # => reuse=True here so THIS bind can't fail  # fmt: skip
peer = socket.create_connection((HOST, PORT), timeout=5)  # => a real client triggers accept()  # fmt: skip
conn, _ = first_server.accept()  # => completes the handshake peer's connect() started above  # fmt: skip
conn.close()  # => the SERVER actively closes first -- this side now owns the TIME_WAIT socket
peer.close()  # => the client's own socket also closes -- irrelevant to which SIDE owns TIME_WAIT
first_server.close()  # => the listening socket itself is also closed now

# Step 2: immediately try to bind a SECOND socket to the exact same port WITHOUT reuse.
try:
    second_server = bind_serve_and_close(reuse=False)  # => no SO_REUSEADDR set this time  # fmt: skip
    second_server.close()  # => only reached if bind() above did NOT raise
    without_reuse_result = "bind succeeded"  # => on this OS/timing, no collision occurred  # fmt: skip
except OSError as err:
    without_reuse_result = f"bind FAILED: {err}"  # => the expected "Address already in use"  # fmt: skip
print(f"without SO_REUSEADDR: {without_reuse_result}")

# Step 3: the SAME immediate re-bind, but WITH SO_REUSEADDR set -- this one must succeed.
third_server = bind_serve_and_close(reuse=True)  # => SO_REUSEADDR: reuse a TIME_WAIT port  # fmt: skip
print("with SO_REUSEADDR: bind succeeded")  # => reaching this line at all proves bind() worked  # fmt: skip
third_server.close()  # => releases the final socket -- nothing else in this script needs it

print("ex-38 OK")  # => confirms both the failure and the fix were genuinely reproduced
