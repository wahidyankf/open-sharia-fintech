"""Example 37: Graceful Close -- Detecting an Empty recv()."""

import socket  # => stdlib sockets -- an empty recv() is the signal this whole example turns on
import threading  # => only the ready-signal + background thread, not real concurrency

HOST = "127.0.0.1"  # => loopback -- keeps this graceful-close demo local and deterministic  # fmt: skip
PORT = 50037  # => co-05: a fresh ephemeral port, unique to this example


def server(ready: threading.Event, observed: list[str]) -> None:  # => "observed" is the shared log  # fmt: skip
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
            while True:  # => co-07: loops until the connection itself signals it is done  # fmt: skip
                data = conn.recv(1024)  # => reads whatever is available -- returns b'' on close  # fmt: skip
                if not data:  # => co-10: recv() returning b'' means the PEER closed its side  # fmt: skip
                    observed.append("empty recv -- peer closed, exiting loop cleanly")  # => logged  # fmt: skip
                    break  # => this is the CORRECT, graceful way to end a server's read loop
                observed.append(f"received {data!r}")  # => logs every message that arrives before close  # fmt: skip


ready_event = threading.Event()
log: list[str] = []  # => records what the server observed, for the assertions below
thread = threading.Thread(target=server, args=(ready_event, log), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the client code that sends-then-closes below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

sock = socket.create_connection((HOST, PORT), timeout=5)
# => connect() outside a "with" block here, since it must stay open until the explicit close below
sock.sendall(b"one message before closing")  # => one real message ...
sock.close()  # => ... then the client closes -- no explicit "goodbye" message is sent at all

thread.join(timeout=5)  # => waits for the server's loop to actually observe the close and exit  # fmt: skip

for line in log:  # => replays the server thread's observations back on the main thread
    print(line)  # => replays every event the server's read loop recorded, in order

assert log[-1] == "empty recv -- peer closed, exiting loop cleanly"  # => confirms clean shutdown  # fmt: skip
print("ex-37 OK")  # => confirms the server's loop exited via the graceful path, not a crash  # fmt: skip
