"""Example 40: A Thread per Client -- Serving Two Clients Simultaneously."""

import socket  # => stdlib sockets -- one thread per accepted connection is what changes here
import threading  # => the actual fix for Example 39's sequential-serving problem
import time  # => wall-clock timing is what proves concurrent, not sequential, serving

HOST = "127.0.0.1"  # => loopback -- keeps this concurrency demo local and deterministic
PORT = 50040  # => co-05: a fresh ephemeral port, unique to this example


def handle_client(conn: socket.socket, delay: float) -> None:  # => runs on its OWN thread  # fmt: skip
    with conn:  # => this handler's own connection -- closes automatically on block exit
        data = conn.recv(1024)  # => blocks only THIS thread -- other handler threads are unaffected  # fmt: skip
        time.sleep(delay)  # => simulates slow per-client work -- does NOT block other clients  # fmt: skip
        conn.sendall(data.upper())  # => the same trivial per-client transformation as Example 39  # fmt: skip


def server(ready: threading.Event, delays: list[float]) -> None:  # => one thread spawned per delay  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        # => IPv4 + TCP, scoped to this "with" block so the fd always closes on exit
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => set BEFORE bind() -- lets an immediate re-run reuse a TIME_WAIT'd port
        sock.bind((HOST, PORT))
        # => claims (HOST, PORT) for this process -- must happen before listen()
        sock.listen(5)
        # => flips the socket passive, ready to queue several pending connections
        ready.set()
        # => unblocks the main thread's wait() below -- no guessed sleep() needed
        handlers: list[threading.Thread] = []  # => one thread PER accepted connection (co-10)  # fmt: skip
        for delay in delays:  # => accept exactly two clients, then stop
            conn, _ = sock.accept()  # => accept() itself is still sequential, one at a time  # fmt: skip
            handler = threading.Thread(target=handle_client, args=(conn, delay))  # => co-10: NOT run yet  # fmt: skip
            handler.start()  # => handling happens CONCURRENTLY once each thread starts
            handlers.append(handler)  # => tracked so the loop below can wait for every one  # fmt: skip
        for handler in handlers:  # => waits for BOTH handler threads, not just the last one started  # fmt: skip
            handler.join(timeout=5)  # => waits for every spawned handler thread to finish  # fmt: skip


def client(name: bytes, results: dict[bytes, float]) -> None:  # => same shape as Example 39's  # fmt: skip
    start = time.monotonic()  # => this client's own local clock, for relative timing
    sock = socket.create_connection((HOST, PORT), timeout=5)  # => connects immediately
    sock.sendall(name)  # => no artificial client-side delay this time -- the SERVER delays now  # fmt: skip
    sock.recv(1024)  # => only returns once its OWN handler thread has replied
    results[name] = time.monotonic() - start  # => total time from connect to being served  # fmt: skip
    sock.close()  # => releases this client's socket once its own round trip is done


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
# Both clients get a 0.3s server-side delay -- if they were served SEQUENTIALLY, the total
# wall-clock time for both to finish would be roughly 0.6s; served CONCURRENTLY, roughly 0.3s.
server_thread = threading.Thread(target=server, args=(ready_event, [0.3, 0.3]), daemon=True)  # fmt: skip
# => daemon=True: this thread never blocks process exit if something above hangs
server_thread.start()
# => runs the server concurrently with the two client threads started below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

results: dict[bytes, float] = {}  # => co-01: measured, not assumed, per-client round-trip times  # fmt: skip
overall_start = time.monotonic()  # => a SEPARATE clock measuring both clients TOGETHER
client_c = threading.Thread(target=client, args=(b"C", results))  # => C's own thread, unstarted  # fmt: skip
client_d = threading.Thread(target=client, args=(b"D", results))  # => D's own thread, unstarted  # fmt: skip
client_c.start()  # => C's connect() begins racing D's, just like the server's two handlers
client_d.start()  # => D's connect() begins concurrently, immediately after C's
client_c.join(timeout=5)  # => waits for C's full round trip, including its 0.3s server delay  # fmt: skip
client_d.join(timeout=5)  # => waits for D's full round trip, including its own 0.3s server delay  # fmt: skip
overall_elapsed = time.monotonic() - overall_start  # => the aggregate proof of concurrency  # fmt: skip
server_thread.join(timeout=5)  # => waits for the server to have handled both connections  # fmt: skip

print(f"client C time: {results[b'C']:.3f}s")  # => expect roughly 0.3s, C's own server delay  # fmt: skip
print(f"client D time: {results[b'D']:.3f}s")  # => expect roughly 0.3s too, served concurrently  # fmt: skip
print(f"overall wall-clock for BOTH clients: {overall_elapsed:.3f}s")  # => expect ~0.3s, not ~0.6s  # fmt: skip

# If the two 0.3s delays ran sequentially, overall_elapsed would be close to 0.6s.
# Running concurrently, it stays close to 0.3s -- proving both were served AT THE SAME TIME.
assert overall_elapsed < 0.55  # => well under the 0.6s a sequential server would have taken  # fmt: skip
print("ex-40 OK")  # => confirms the aggregate-time proof of concurrency held for this run  # fmt: skip
