"""Example 35: Multiple Messages, One Connection, In Order."""

import socket  # => stdlib sockets -- this example reuses Example 33's read_line() framing
import threading  # => only the ready-signal + background thread, not real concurrency


HOST = "127.0.0.1"  # => loopback -- keeps this multi-message demo local and deterministic  # fmt: skip
PORT = 50035  # => co-05: a fresh ephemeral port, unique to this example


def read_line(sock: socket.socket, buffer: bytearray) -> bytes:  # => same framing as Example 33  # fmt: skip
    while b"\n" not in buffer:  # => keep reading until a full line has actually arrived
        chunk = sock.recv(64)  # => reads whatever is available, up to 64 bytes at a time  # fmt: skip
        if not chunk:  # => the peer closed before a full line arrived
            raise ConnectionError("peer closed mid-line")
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one line, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the NEXT call  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


def server(ready: threading.Event) -> None:  # => co-11: many messages, ONE persistent connection  # fmt: skip
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
            buf = bytearray()  # => ONE buffer shared across all three messages on this connection  # fmt: skip
            for _ in range(3):  # => the client sends exactly 3 lines -- reply to each in turn  # fmt: skip
                line = read_line(conn, buf)  # => co-07: TCP guarantees these arrive IN ORDER  # fmt: skip
                reply = line.upper() + b"\n"  # => a trivial per-message transformation
                conn.sendall(reply)  # => each request gets its own response before the next arrives  # fmt: skip


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the client code that sends three messages below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

replies: list[bytes] = []  # => co-01: measured responses, one per message, in receipt order  # fmt: skip
with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => a plain, ordinary connect()  # fmt: skip
    buf = bytearray()  # => the CLIENT's own leftover-bytes buffer -- separate from the server's  # fmt: skip
    for word in (b"first", b"second", b"third"):  # => three separate messages, one connection  # fmt: skip
        sock.sendall(word + b"\n")  # => sent one at a time, waiting for each reply
        replies.append(read_line(sock, buf))  # => waits for THIS message's reply before looping  # fmt: skip
        print(f"client got: {replies[-1]!r}")  # => confirms each reply arrives before the next send  # fmt: skip

thread.join(timeout=5)
# => waits for the server thread to finish handling all three messages before exiting

assert replies == [b"FIRST", b"SECOND", b"THIRD"]  # => confirms strict request/response order  # fmt: skip
# a single persistent connection, not three separate connect()s, is what this example exists
# to demonstrate -- the same socket and buffer carry all three request/response round trips.
print("ex-35 OK")  # => confirms all three messages round-tripped in order, unmodified beyond upper()  # fmt: skip
