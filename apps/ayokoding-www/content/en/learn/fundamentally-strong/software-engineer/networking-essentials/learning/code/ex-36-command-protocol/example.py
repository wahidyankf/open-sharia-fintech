"""Example 36: A Tiny Command Protocol -- PING/PONG and TIME."""

import socket  # => stdlib sockets -- this example builds a protocol ON TOP of it
import threading  # => only the ready-signal + background thread, not real concurrency
import time  # => TIME's reply is real wall-clock state, not an echo of client input


HOST = "127.0.0.1"  # => loopback -- keeps this protocol demo local and deterministic
PORT = 50036  # => co-05: a fresh ephemeral port, unique to this example


def read_line(sock: socket.socket, buffer: bytearray) -> bytes:  # => same framing as Example 33  # fmt: skip
    while b"\n" not in buffer:  # => keep reading until a full command line has arrived
        chunk = sock.recv(64)  # => reads whatever is available, up to 64 bytes at a time  # fmt: skip
        if not chunk:  # => the peer closed before a full line arrived
            raise ConnectionError("peer closed mid-line")
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one command, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the NEXT command  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


def handle_command(command: bytes) -> bytes:  # => co-01, co-11: a tiny request/response protocol  # fmt: skip
    if command == b"PING":  # => the simplest possible liveness check
        return b"PONG"  # => a FIXED reply -- the same for every PING, unlike TIME below
    if command == b"TIME":  # => a command that returns SERVER-side state, not an echo
        return str(int(time.time())).encode()  # => Unix epoch seconds, as ASCII digits
    return b"ERR unknown command"  # => co-01: the server, not the client, decides what's valid


def server(ready: threading.Event) -> None:  # => backgrounded so the client below can run inline  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        # => IPv4 + TCP, scoped to this "with" block so the fd always closes on exit
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => set BEFORE bind() -- lets an immediate re-run reuse a TIME_WAIT'd port
        sock.bind((HOST, PORT))
        # => claims (HOST, PORT) for this process -- must happen before listen()
        sock.listen(1)
        # => flips the socket passive, ready to queue one pending connection
        ready.set()
        # => unblocks the main thread's wait() below -- no guessed sleep() needed
        conn, _ = sock.accept()
        # => BLOCKS until the client's connect() completes the TCP handshake
        with conn:  # => this one connection's socket -- closes automatically on block exit  # fmt: skip
            buf = bytearray()  # => ONE buffer shared across both commands on this connection  # fmt: skip
            for _ in range(2):  # => this client sends exactly two commands, PING then TIME  # fmt: skip
                command = read_line(conn, buf)  # => reads ONE command line at a time
                conn.sendall(handle_command(command) + b"\n")  # => reply, then wait for the next  # fmt: skip


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the client code that sends PING/TIME below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => a plain, ordinary connect()  # fmt: skip
    buf = bytearray()  # => the CLIENT's own leftover-bytes buffer -- separate from the server's  # fmt: skip
    sock.sendall(b"PING\n")  # => request 1: a liveness check
    ping_reply = read_line(sock, buf)  # => waits for the server's fixed PONG reply
    print(f"PING -> {ping_reply!r}")  # => expect the same PONG every single run

    sock.sendall(b"TIME\n")  # => request 2: ask the server for its current time
    time_reply = read_line(sock, buf)  # => waits for the server's dynamic epoch-timestamp reply  # fmt: skip
    print(f"TIME -> {time_reply!r}")  # => expect a DIFFERENT number each run, unlike PING's PONG  # fmt: skip

thread.join(timeout=5)
# => waits for the server thread to finish handling both commands before exiting

assert ping_reply == b"PONG"  # => confirms the fixed-response command
assert time_reply.isdigit()  # => confirms TIME returned a plausible-looking epoch timestamp  # fmt: skip
print("ex-36 OK")  # => confirms both request/reply pairs completed correctly over one connection  # fmt: skip
