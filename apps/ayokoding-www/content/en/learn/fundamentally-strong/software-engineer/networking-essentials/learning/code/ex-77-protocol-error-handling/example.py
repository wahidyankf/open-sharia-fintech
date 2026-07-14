"""Example 77: A Malformed Command Gets an Error Reply, Not a Crash."""  # => co-01/co-11

import socket  # => stdlib sockets -- the error-reply behavior lives entirely in application code
import threading  # => only the ready-signal + background thread, not real concurrency

HOST = (
    "127.0.0.1"  # => loopback -- keeps this error-handling demo local and deterministic
)
PORT = 50077  # => co-05: a fresh ephemeral port, unique to this example


def read_line(
    sock: socket.socket, buffer: bytearray
) -> bytes:  # => same framing as Example 33
    while b"\n" not in buffer:  # => keep reading until a full command line has arrived
        chunk = sock.recv(
            64
        )  # => reads whatever is available, up to 64 bytes at a time
        if not chunk:  # => the peer closed before a full line arrived
            raise ConnectionError(
                "peer closed mid-line"
            )  # => a genuinely EXCEPTIONAL framing error
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(
        b"\n"
    )  # => split off exactly one command, keep the remainder
    buffer[:] = (
        rest  # => whatever came AFTER the newline stays buffered for the NEXT command
    )
    return bytes(
        line
    )  # => bytearray.partition returns bytearray -- normalize to plain bytes


def handle_command(
    command: bytes,
) -> bytes:  # => co-01/co-11: the server DECIDES what's valid
    if command == b"PING":  # => the simplest possible liveness check
        return b"PONG"  # => a FIXED reply -- the same for every PING, unlike TIME below
    if command == b"TIME":  # => a command that returns SERVER-side state, not an echo
        return b"1234567890"  # => a FIXED stand-in reply -- this example is about errors, not clocks
    return (
        b"ERR unknown command: " + command
    )  # => a graceful, protocol-level error reply


def server(
    ready: threading.Event,
) -> None:  # => co-11: never crashes, whatever the client sends
    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as sock:  # => same triple as Ex 29+
        sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # => same boilerplate as before
        sock.bind((HOST, PORT))  # => claims (HOST, PORT) for this process
        sock.listen(
            1
        )  # => flips the socket passive, ready to queue one pending connection
        ready.set()  # => unblocks the main thread's wait() below -- no guessed sleep() needed
        conn, _ = (
            sock.accept()
        )  # => BLOCKS until the client's connect() completes the handshake
        with (
            conn
        ):  # => this one connection's socket -- closes automatically on block exit
            buf = (
                bytearray()
            )  # => ONE buffer shared across both commands on this connection
            for _ in range(
                2
            ):  # => this client sends one BAD command, then one GOOD command
                command = read_line(conn, buf)  # => reads ONE command line at a time
                reply = handle_command(
                    command
                )  # => never raises -- always returns SOME reply
                conn.sendall(
                    reply + b"\n"
                )  # => reply, then wait for the next -- no early close


ready_event = (
    threading.Event()
)  # => the same ready-signal pattern used since Example 34
thread = threading.Thread(
    target=server, args=(ready_event,), daemon=True
)  # => co-11: unstarted yet
thread.start()  # => runs the server concurrently with the two-command client code below
ready_event.wait(timeout=5)  # => blocks until bind()+listen() genuinely completed

with socket.create_connection(
    (HOST, PORT), timeout=5
) as sock:  # => a plain, ordinary connect()
    buf = (
        bytearray()
    )  # => the CLIENT's own leftover-bytes buffer -- separate from the server's
    sock.sendall(b"BOGUS\n")  # => a malformed / unrecognized command
    bad_reply = read_line(
        sock, buf
    )  # => waits for the server's ERR reply, not a dropped connection
    print(
        f"BOGUS -> {bad_reply!r}"
    )  # => shows the ERR reply, proving no crash occurred

    sock.sendall(
        b"PING\n"
    )  # => the SAME connection still works afterward -- no crash occurred
    good_reply = read_line(
        sock, buf
    )  # => waits for a NORMAL reply, proving the session survived
    print(
        f"PING -> {good_reply!r}"
    )  # => shows the SAME connection still answering normally

thread.join(
    timeout=5
)  # => waits for the server thread to finish handling both commands

assert bad_reply.startswith(
    b"ERR"
)  # => confirms a clear error reply, not a dropped connection
assert (
    good_reply == b"PONG"
)  # => confirms the connection survived the bad command entirely
print(
    "ex-77 OK"
)  # => confirms one malformed command didn't corrupt the rest of the session
