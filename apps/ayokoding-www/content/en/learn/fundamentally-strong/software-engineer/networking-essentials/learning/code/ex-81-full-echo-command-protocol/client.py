"""Example 81: Full Command Client -- Sends PING and TIME, Then Shuts Down Gracefully."""  # => co-07

import socket  # => stdlib sockets -- this client's own copy of the same read_line() framing

HOST = "127.0.0.1"  # => loopback -- matches server.py's own HOST exactly
PORT = 50081  # => co-05: matches server.py's own PORT exactly


def read_line(sock: socket.socket, buffer: bytearray) -> bytes:  # => same framing as Example 33  # fmt: skip
    while b"\n" not in buffer:  # => keep reading until a full reply line has arrived
        chunk = sock.recv(64)  # => reads whatever is available, up to 64 bytes at a time  # fmt: skip
        if not chunk:  # => the peer closed before a full line arrived
            return b""  # => an EMPTY line signals "peer closed" up to the caller
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one reply, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the NEXT reply  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


def run_client(client_name: str) -> list[bytes]:  # => "client_name" only labels this run's output  # fmt: skip
    replies: list[bytes] = []  # => co-01: measured, not assumed, one reply per command sent  # fmt: skip
    with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => co-07: one connection  # fmt: skip
        buf = bytearray()  # => this client's own leftover-bytes buffer, private to this run  # fmt: skip
        for command in (b"PING", b"TIME"):  # => two commands over the ONE connection (co-11)  # fmt: skip
            sock.sendall(command + b"\n")  # => sends this command, then waits for its own reply  # fmt: skip
            replies.append(read_line(sock, buf))  # => waits for THIS command's reply before looping  # fmt: skip
        # Exiting the `with` block calls close() -- co-07: this is the GRACEFUL shutdown
        # the server's read_line() detects as an empty recv() and handles cleanly.
    print(f"{client_name}: PING -> {replies[0]!r}, TIME -> {replies[1]!r}")  # => both replies at once  # fmt: skip
    return replies  # => both replies, for the caller's own assertions below


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    replies = run_client("client")  # => a real connection to the real server.py process
    assert replies[0] == b"PONG"  # => confirms PING got its fixed reply
    assert replies[1].isdigit()  # => confirms TIME returned a plausible-looking epoch timestamp  # fmt: skip
    print("ex-81 client OK")  # => confirms both commands round-tripped over one connection  # fmt: skip
