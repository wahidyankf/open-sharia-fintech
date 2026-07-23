"""Example 39: A Sequential Accept Loop -- One Client at a Time."""

import socket  # => stdlib sockets -- accept() itself is what serializes clients here
import threading  # => runs BOTH clients concurrently, so their queueing is genuinely observable
import time  # => wall-clock timing is what actually proves the sequential-server claim

HOST = "127.0.0.1"  # => loopback -- keeps this backlog-queueing demo local and deterministic
PORT = 50039  # => co-05: a fresh ephemeral port, unique to this example


def server(ready: threading.Event) -> None:  # => co-01: a SINGLE-threaded accept loop
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        # => IPv4 + TCP, scoped to this "with" block so the fd always closes on exit
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => set BEFORE bind() -- lets an immediate re-run reuse a TIME_WAIT'd port
        sock.bind((HOST, PORT))
        # => claims (HOST, PORT) for this process -- must happen before listen()
        sock.listen(5)  # => backlog of 5 -- client B can QUEUE here while client A is served  # fmt: skip
        ready.set()
        # => unblocks the main thread's wait() below -- no guessed sleep() needed
        for _ in range(2):  # => this demo serves exactly two clients, one at a time
            conn, _ = sock.accept()  # => blocks until the NEXT client is ready to be served  # fmt: skip
            with conn:  # => this one connection's socket -- closes automatically on block exit  # fmt: skip
                data = conn.recv(1024)  # => blocks HERE until this client actually sends  # fmt: skip
                # => while blocked above, any OTHER client that already connected just waits
                # => in the OS backlog queue -- accept() for them has not been called yet
                conn.sendall(data.upper())  # => the ONLY per-client work: uppercase and reply  # fmt: skip


def client(name: bytes, delay_before_send: float, results: dict[bytes, float]) -> None:
    # => delay_before_send lets this test CONTROL which client stalls the server
    start = time.monotonic()  # => this client's own local clock, for relative timing
    sock = socket.create_connection((HOST, PORT), timeout=5)  # => connects immediately
    time.sleep(delay_before_send)  # => client A stalls here, holding up the server's recv()  # fmt: skip
    sock.sendall(name)  # => sent only AFTER the deliberate stall above, if any
    sock.recv(1024)  # => only returns once the server has actually served THIS client
    results[name] = time.monotonic() - start  # => total time from connect to being served  # fmt: skip
    sock.close()  # => releases this client's socket once its own round trip is done


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
server_thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
server_thread.start()
# => runs the server concurrently with the two client threads started below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

results: dict[bytes, float] = {}  # => co-01: measured, not assumed, per-client round-trip times  # fmt: skip
client_a = threading.Thread(target=client, args=(b"A", 0.3, results))
# => connects first, but STALLS 0.3s before sending -- holds the server's recv() hostage
client_b = threading.Thread(target=client, args=(b"B", 0.0, results))
# => connects right after A, sends IMMEDIATELY, but must still wait in the backlog

client_a.start()  # => A's thread starts running -- its stall hasn't begun yet
time.sleep(0.05)  # => a tiny head start so A's connection is accepted before B's arrives  # fmt: skip
client_b.start()  # => B's thread starts, and B's connect() races A's ongoing stall
client_a.join(timeout=5)  # => waits for A's full round trip (connect, stall, send, recv) to finish  # fmt: skip
client_b.join(timeout=5)  # => waits for B's full round trip, including its queued wait, to finish  # fmt: skip
server_thread.join(timeout=5)  # => waits for the server to have served both clients

print(f"client A total time: {results[b'A']:.3f}s")  # => expect roughly 0.3s, A's own stall  # fmt: skip
print(f"client B total time: {results[b'B']:.3f}s")  # => expect roughly 0.3s too, from QUEUEING  # fmt: skip

# B connected almost immediately but couldn't be SERVED until A's slow recv() finished --
# so B's total time is dominated by A's delay, not by B's own (zero) delay.
assert results[b"B"] >= 0.2  # => B's wait proves it queued behind A, not merely its own path  # fmt: skip
print("ex-39 OK")  # => confirms the sequential-serving claim was measured, not just asserted  # fmt: skip
