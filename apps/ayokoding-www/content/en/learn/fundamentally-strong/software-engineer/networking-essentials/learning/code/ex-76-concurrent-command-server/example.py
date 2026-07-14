"""Example 76: The Command Server, Extended to Serve Clients Concurrently."""

import socket  # => stdlib sockets -- every layer this whole capstone-style server builds on
import threading  # => co-10: one thread PER accepted client, exactly Example 40's fix
import time  # => TIME's reply is real wall-clock state; the delay/elapsed timings use it too

HOST = "127.0.0.1"  # => loopback -- keeps this concurrency demo local and deterministic
PORT = 50076  # => co-05: a fresh ephemeral port, unique to this example


def read_line(sock: socket.socket, buffer: bytearray) -> bytes:  # => same framing as Example 33  # fmt: skip
    while b"\n" not in buffer:  # => keep reading until a full command line has arrived
        chunk = sock.recv(64)  # => reads whatever is available, up to 64 bytes at a time  # fmt: skip
        if not chunk:  # => the peer closed before a full line arrived
            raise ConnectionError("peer closed mid-line")
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one command, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the NEXT command  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


def handle_command(command: bytes) -> bytes:  # => the same PING/TIME protocol as Example 36  # fmt: skip
    if command == b"PING":  # => the simplest possible liveness check
        return b"PONG"  # => a FIXED reply -- the same for every PING, unlike TIME below
    if command == b"TIME":  # => a command that returns SERVER-side state, not an echo
        return str(int(time.time())).encode()  # => Unix epoch seconds, as ASCII digits
    return b"ERR unknown command"  # => co-01: the server, not the client, decides what's valid


def handle_client(conn: socket.socket, delay: float) -> None:  # => co-10: runs on ITS OWN thread  # fmt: skip
    with conn:  # => this handler's own connection -- closes automatically on block exit
        buf = bytearray()  # => this client's own leftover-bytes buffer, private to its thread  # fmt: skip
        command = read_line(conn, buf)  # => blocks only THIS thread while waiting for a command  # fmt: skip
        time.sleep(delay)  # => simulates one client being slower than the other
        conn.sendall(handle_command(command) + b"\n")  # => reply, once this thread's delay elapses  # fmt: skip


def server(ready: threading.Event) -> None:  # => co-01: one thread spawned per accepted client  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => same boilerplate as before  # fmt: skip
        sock.bind((HOST, PORT))  # => claims (HOST, PORT) for this process
        sock.listen(5)  # => backlog large enough for both clients to queue if needed
        ready.set()  # => unblocks the main thread's wait() below -- no guessed sleep() needed
        handlers: list[threading.Thread] = []  # => one thread PER accepted connection (co-10)  # fmt: skip
        # Whichever client connects first gets the 0.3s delay -- which PHYSICAL client (A or
        # B) that turns out to be depends on OS scheduling, but the concurrency proof below
        # doesn't depend on knowing that in advance: it only depends on the TOTAL wall-clock.
        for delay in (0.3, 0.0):  # => accept exactly two clients, one delayed, one immediate  # fmt: skip
            conn, _ = sock.accept()  # => accept() itself is still sequential, one at a time  # fmt: skip
            handler = threading.Thread(target=handle_client, args=(conn, delay))  # => co-10: unstarted  # fmt: skip
            handler.start()  # => co-01: each client is served on its OWN thread, concurrently
            handlers.append(handler)  # => tracked so the loop below can wait for every one  # fmt: skip
        for handler in handlers:  # => waits for BOTH handler threads, not just the last started  # fmt: skip
            handler.join(timeout=5)  # => waits for every spawned handler thread to finish  # fmt: skip


def client(name: bytes, command: bytes, results: dict[bytes, tuple[bytes, float]]) -> None:  # fmt: skip
    # => "results" is shared across both client threads, keyed by name
    start = time.monotonic()  # => this client's own local clock, for relative timing
    sock = socket.create_connection((HOST, PORT), timeout=5)  # => connects immediately
    sock.sendall(command + b"\n")  # => sends this client's own command, e.g. PING
    buf = bytearray()  # => this client's own leftover-bytes buffer -- separate from the server's  # fmt: skip
    reply = read_line(sock, buf)  # => blocks until this client's OWN handler thread replies  # fmt: skip
    elapsed = time.monotonic() - start  # => total time from connect to being served, for THIS client  # fmt: skip
    results[name] = (reply, elapsed)  # => stores both the reply AND the timing, keyed by name  # fmt: skip
    sock.close()  # => releases this client's socket once its own round trip is done


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
server_thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
server_thread.start()  # => runs the server concurrently with the two client threads below
ready_event.wait(timeout=5)  # => blocks until bind()+listen() genuinely completed

results: dict[bytes, tuple[bytes, float]] = {}  # => co-01: measured, not assumed, per-client timing  # fmt: skip
overall_start = time.monotonic()  # => a SEPARATE clock measuring both clients TOGETHER
thread_a = threading.Thread(target=client, args=(b"A", b"PING", results))  # => A's own thread  # fmt: skip
thread_b = threading.Thread(target=client, args=(b"B", b"PING", results))  # => B's own thread  # fmt: skip
thread_a.start()  # => A's connect() begins racing B's, just like the server's two handlers
thread_b.start()  # => B's connect() begins concurrently, immediately after A's
thread_a.join(timeout=5)  # => waits for A's full round trip to finish
thread_b.join(timeout=5)  # => waits for B's full round trip to finish
overall_elapsed = time.monotonic() - overall_start  # => the aggregate proof of concurrency  # fmt: skip
server_thread.join(timeout=5)  # => waits for the server to have handled both connections  # fmt: skip

a_reply, a_elapsed = results[b"A"]  # => unpacks A's own (reply, elapsed) tuple
b_reply, b_elapsed = results[b"B"]  # => unpacks B's own (reply, elapsed) tuple
print(f"client A: reply={a_reply!r}, elapsed={a_elapsed:.3f}s")
print(f"client B: reply={b_reply!r}, elapsed={b_elapsed:.3f}s")
print(f"overall wall-clock for BOTH clients: {overall_elapsed:.3f}s")

assert a_reply == b"PONG"  # => confirms A's command genuinely round-tripped through the server  # fmt: skip
assert b_reply == b"PONG"  # => confirms B's command genuinely round-tripped through the server  # fmt: skip
# co-01: if the two clients were served SEQUENTIALLY, overall time would approach 0.3s (one
# delay) PLUS B's own time; served concurrently, B finishes almost immediately regardless of A.
assert overall_elapsed < 0.5  # => well under the ~0.6s a sequential server would have taken  # fmt: skip
print("ex-76 OK")  # => confirms the PING/TIME protocol survived being served concurrently  # fmt: skip
