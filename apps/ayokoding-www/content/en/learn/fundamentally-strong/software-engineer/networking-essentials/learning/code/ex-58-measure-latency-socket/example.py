"""Example 58: Measure a TCP Round Trip in Python."""

import socket  # => stdlib sockets -- the round trip being timed is a plain send/recv pair
import threading  # => only the ready-signal + background thread, not real concurrency
import time  # => perf_counter() is the actual measurement instrument this example turns on

HOST = "127.0.0.1"  # => loopback -- gives a latency FLOOR, not a real-network figure
PORT = 50058  # => co-05: a fresh ephemeral port, unique to this example
# a real network hop would add real transit time on top of this floor -- this measures pure
# socket + OS overhead, the minimum any TCP round trip on this machine could possibly cost.


def server(ready: threading.Event) -> None:  # => backgrounded so the client below can run inline  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
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
        with conn:  # => a context manager -- conn's fd closes automatically when this block exits
            for _ in range(5):  # => this demo measures 5 separate round trips
                data = conn.recv(64)
                if not data:
                    break
                conn.sendall(data)  # => echoes back as fast as possible -- no artificial delay  # fmt: skip


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the timed client loop that follows below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

latencies_ms: list[float] = []  # => co-01: measured, not assumed, exactly like Example 24 did  # fmt: skip
# perf_counter() (not time.time()) is used because it's monotonic and immune to clock adjustments.
with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => one connection, reused below  # fmt: skip
    for i in range(5):  # => five independent measurements smooth out one-off scheduling jitter  # fmt: skip
        start = time.perf_counter()  # => a high-resolution clock, appropriate for sub-ms timing  # fmt: skip
        sock.sendall(b"ping")  # => a tiny 4-byte payload -- measures overhead, not bandwidth  # fmt: skip
        sock.recv(64)  # => blocks until the echoed reply arrives
        # 64 bytes comfortably exceeds the 4-byte payload -- no partial-read handling needed here.
        elapsed_ms = (time.perf_counter() - start) * 1000  # => convert seconds to milliseconds  # fmt: skip
        latencies_ms.append(elapsed_ms)  # => accumulated across all 5 iterations for the average  # fmt: skip
        print(f"round trip {i + 1}: {elapsed_ms:.3f} ms")  # => per-iteration figure shows jitter  # fmt: skip

thread.join(timeout=5)
# => waits for the server thread to finish handling all five round trips before exiting

average_ms = sum(latencies_ms) / len(latencies_ms)  # => a simple mean across the 5 measurements  # fmt: skip
# a genuine average of REAL measurements, not a hand-picked "looks about right" number.
print(f"average: {average_ms:.3f} ms")  # => the single headline number this example exists to produce  # fmt: skip

assert all(ms >= 0 for ms in latencies_ms)  # => sanity check: time never runs backward
assert average_ms < 50  # => loopback round trips are consistently well under 50ms
print("ex-58 OK")  # => confirms all five round trips were measured and stayed within bounds  # fmt: skip
