"""Example 32: socket.connect / .sendall / .recv, Annotated."""

import socket  # => same stdlib module as every other socket example in this tier
import threading  # => only for the ready-signal + background thread, not real concurrency

HOST = "127.0.0.1"  # => loopback -- this whole exchange stays on the local machine
PORT = 50032  # => co-05: a fresh ephemeral port, distinct from every other example's port  # fmt: skip


def server(ready: threading.Event) -> None:  # => a minimal echo server, backgrounded (co-10)  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # => IPv4 + TCP -- scoped to this "with" block so the fd always closes, even on error
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => must be set BEFORE bind(), or an immediate re-run could fail with "address in use"
        sock.bind((HOST, PORT))
        # => claims this exact (HOST, PORT) pair for this process -- fails if already taken
        sock.listen(1)
        # => flips the socket passive: it can now queue ONE pending connection before accept()
        ready.set()
        # => signals the main thread it is safe to connect -- avoids a guessed sleep() delay
        conn, _ = sock.accept()
        # => BLOCKS here until the client's connect() below completes the three-way handshake
        with conn:
            # => conn is this ONE client's private socket -- distinct from the listening sock
            data = conn.recv(1024)  # => reads whatever the client sends
            conn.sendall(data)  # => echoes it straight back


ready_event = threading.Event()
# => a real synchronization primitive -- co-11: avoids the "sleep(1) and hope" anti-pattern
server_thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this background thread never blocks process exit if something hangs
server_thread.start()
# => runs the server concurrently with the connect/send/recv code that follows below
ready_event.wait(timeout=5)
# => blocks the main thread here until bind()+listen() have both genuinely completed

# create_connection wraps getaddrinfo + socket() + connect() in one call (co-01, co-10).
with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => connect: the TCP handshake  # fmt: skip
    # => connect() blocks until the three-way handshake (SYN, SYN-ACK, ACK) completes (co-07)
    print("state: connected")  # => Output line 1
    sock.sendall(b"round trip\n")  # => sendall: loops internally until EVERY byte is written  # fmt: skip
    # => a plain .send() can write FEWER bytes than requested; .sendall() never does
    reply = sock.recv(1024)  # => recv: reads up to 1024 bytes, blocking until at least 1 arrives  # fmt: skip
    # => recv's argument is a MAXIMUM, not a guarantee -- it can return fewer bytes than asked
    print(f"state: received {reply!r}")  # => Output line 2

server_thread.join(timeout=5)
# => waits here for the server thread to finish handling that one client before exiting

assert reply == b"round trip\n"  # => confirms the full round trip preserved every byte
print("ex-32 OK")  # => a final marker confirming the assertion above passed, not just ran  # fmt: skip
