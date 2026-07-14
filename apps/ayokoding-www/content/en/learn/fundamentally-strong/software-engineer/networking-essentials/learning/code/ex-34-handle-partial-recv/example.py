"""Example 34: Handle Partial recv() -- Reassemble a Large Message."""

import socket  # => stdlib sockets -- recv_exact below is built entirely on top of it
import threading  # => only the ready-signal + background thread, not real concurrency

HOST = "127.0.0.1"  # => loopback -- keeps this large-payload demo local and deterministic  # fmt: skip
PORT = 50034  # => co-05: a fresh ephemeral port, unique to this example
PAYLOAD_SIZE = 200_000  # => far bigger than any single recv() call typically returns


def recv_exact(sock: socket.socket, count: int) -> bytes:
    # co-11: recv() may return FEWER bytes than requested for a large payload -- looping
    # until exactly `count` bytes have arrived is the only correct way to read a fixed size.
    chunks: list[bytes] = []  # => collects each partial read
    remaining = count  # => how many more bytes are still needed
    while remaining > 0:  # => keeps looping until the full payload has arrived
        chunk = sock.recv(min(65536, remaining))  # => never over-read past the target size  # fmt: skip
        if not chunk:  # => peer closed before sending everything -- a real, checkable failure  # fmt: skip
            raise ConnectionError("peer closed before sending the full payload")
        chunks.append(chunk)
        # => appended, not concatenated, here -- string/bytes concatenation in a loop is O(n^2)
        remaining -= len(chunk)  # => shrinks toward 0 as more bytes arrive
    return b"".join(chunks)  # => reassembles every partial read into the original bytes, once  # fmt: skip


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
            data = recv_exact(conn, PAYLOAD_SIZE)  # => reassembles the full 200,000-byte payload  # fmt: skip
            intact = data == b"x" * PAYLOAD_SIZE  # => confirms every one of the 200,000 bytes matches  # fmt: skip
            print(f"server received {len(data)} bytes, intact: {intact}")  # => size AND content check  # fmt: skip


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34's peers  # fmt: skip
thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the client connection code that follows below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => a plain, ordinary connect()  # fmt: skip
    sock.sendall(b"x" * PAYLOAD_SIZE)  # => one logical send; the OS may still split it on the wire  # fmt: skip

thread.join(timeout=5)
# => waits for the server thread to finish handling that one client before exiting
print("ex-34 OK")  # => confirms recv_exact() reassembled all 200,000 bytes without loss
