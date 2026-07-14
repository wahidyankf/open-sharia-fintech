"""Example 33: Line Framing with \\n Delimiters."""

import socket  # => stdlib sockets -- this example builds framing ON TOP of it, not inside it
import threading  # => only the ready-signal + background thread, not real concurrency

HOST = "127.0.0.1"  # => loopback -- keeps this framing demo local and deterministic
PORT = 50033  # => co-05: a fresh ephemeral port, unique to this example


def read_line(sock: socket.socket, buffer: bytearray) -> bytes:
    # => a "buffer" parameter, not a local variable, is WHY this survives across MULTIPLE
    # => calls -- leftover bytes past one \n stay available for the NEXT call to read_line
    # A TCP byte stream has NO message boundaries -- co-11 says the protocol must invent
    # its own framing. Here, "one message" means "bytes up to the next newline."
    while b"\n" not in buffer:  # => keep reading until a full line has actually arrived
        chunk = sock.recv(4)  # => a DELIBERATELY tiny read size to force multiple recv() calls  # fmt: skip
        if not chunk:  # => the peer closed before a full line arrived
            raise ConnectionError("peer closed mid-line")
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one line, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the next call  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


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
        with conn:
            buf = bytearray()  # => per-connection leftover-bytes buffer (co-11)
            line = read_line(conn, buf)  # => reassembles ONE full line from many small recv()s  # fmt: skip
            print(f"server framed: {line!r}")  # => proves the tiny 4-byte reads still yield one line  # fmt: skip


ready_event = threading.Event()
thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the client connection code that follows below
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

with socket.create_connection((HOST, PORT), timeout=5) as sock:
    # Sent as ONE call, but the server above reads it back 4 bytes at a time --
    # framing is what makes "a line" meaningful regardless of how recv() chunks it.
    sock.sendall(b"this line spans many tiny reads\n")
    # => sendall guarantees the WHOLE 33-byte line is written, even though the server
    # => on the other end will only ever see it arrive in small, independent chunks

thread.join(timeout=5)
# => waits for the server thread to finish handling that one client before exiting
print("ex-33 OK")  # => confirms read_line() reassembled the tiny reads without loss
