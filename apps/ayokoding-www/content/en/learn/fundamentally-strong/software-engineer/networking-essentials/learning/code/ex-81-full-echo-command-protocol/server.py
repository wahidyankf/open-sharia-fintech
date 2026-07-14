"""Example 81: Full Command Server -- PING/TIME, Multi-Client, Graceful Shutdown."""  # => co-10

import socket  # => stdlib sockets -- every layer this full server/client pair builds on
import threading  # => co-10: one thread PER accepted client, the same fix as Example 40/76
import time  # => TIME's reply is real wall-clock state, not an echo of client input

HOST = "127.0.0.1"  # => loopback -- keeps this server/client demo local and deterministic  # fmt: skip
PORT = 50081  # => co-05: a fresh ephemeral port, unique to this example


def read_line(sock: socket.socket, buffer: bytearray) -> bytes:  # => co-11: line framing  # fmt: skip
    while b"\n" not in buffer:  # => keep reading until a full command line has arrived
        chunk = sock.recv(64)  # => reads whatever is available, up to 64 bytes at a time  # fmt: skip
        if not chunk:  # => co-07: the client closed -- signal it upward as an empty line  # fmt: skip
            return b""  # => an EMPTY line signals "peer closed" up to the caller
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(b"\n")  # => split off exactly one command, keep the remainder  # fmt: skip
    buffer[:] = rest  # => whatever came AFTER the newline stays buffered for the NEXT command  # fmt: skip
    return bytes(line)  # => bytearray.partition returns bytearray -- normalize to plain bytes  # fmt: skip


def handle_command(command: bytes) -> bytes:  # => co-01: the same PING/TIME protocol throughout  # fmt: skip
    if command == b"PING":  # => the simplest possible liveness check
        return b"PONG"  # => a FIXED reply -- the same for every PING, unlike TIME below
    if command == b"TIME":  # => a command that returns SERVER-side state, not an echo
        return str(int(time.time())).encode()  # => Unix epoch seconds, as ASCII digits
    return b"ERR unknown command: " + command  # => a graceful, protocol-level error reply  # fmt: skip


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:  # => co-10: one per client  # fmt: skip
    with conn:  # => this handler's own connection -- closes automatically on block exit
        buf = bytearray()  # => this client's own leftover-bytes buffer, private to its thread  # fmt: skip
        while True:  # => co-07: keeps serving commands until the client disconnects
            command = read_line(conn, buf)  # => reads ONE command line at a time
            if not command:  # => co-07: an empty line means the peer closed -- exit gracefully  # fmt: skip
                break  # => exits the loop -- the "with conn" block then closes gracefully
            conn.sendall(handle_command(command) + b"\n")  # => reply, then wait for the next  # fmt: skip
    print(f"connection from {addr} closed gracefully")  # => runs AFTER the "with" block's close()  # fmt: skip


def run_server(client_count: int) -> None:  # => co-10: serves exactly client_count connections  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => same boilerplate as before  # fmt: skip
        sock.bind((HOST, PORT))  # => claims (HOST, PORT) for this process
        sock.listen(5)  # => backlog large enough for multiple clients to queue if needed  # fmt: skip
        print(f"listening on {HOST}:{PORT}", flush=True)  # => the signal a caller can wait for  # fmt: skip
        handlers: list[threading.Thread] = []  # => one thread PER accepted connection (co-10)  # fmt: skip
        for _ in range(client_count):  # => accepts exactly client_count clients, then stops  # fmt: skip
            conn, addr = sock.accept()  # => accept() itself is still sequential, one at a time  # fmt: skip
            handler = threading.Thread(target=handle_client, args=(conn, addr))  # => co-10: unstarted  # fmt: skip
            handler.start()  # => handling happens CONCURRENTLY once each thread starts
            handlers.append(handler)  # => tracked so the loop below can wait for every one  # fmt: skip
        for handler in handlers:  # => waits for EVERY handler thread, not just the last started  # fmt: skip
            handler.join()  # => waits for every spawned handler thread to finish


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    run_server(client_count=2)  # => this demo serves exactly two concurrent clients, then exits  # fmt: skip
