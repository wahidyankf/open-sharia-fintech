"""Example 81: Full Command Server -- PING/TIME, Multi-Client, Graceful Shutdown."""  # => co-10

import socket  # => stdlib sockets -- every layer this full server/client pair builds on
import threading  # => co-10: one thread PER accepted client, the same fix as Example 40/76
import time  # => TIME's reply is real wall-clock state, not an echo of client input

HOST = (
    "127.0.0.1"  # => loopback -- keeps this server/client demo local and deterministic
)
PORT = 50081  # => co-05: a fresh ephemeral port, unique to this example


def read_line(
    sock: socket.socket, buffer: bytearray
) -> bytes:  # => co-11: line framing
    while b"\n" not in buffer:  # => keep reading until a full command line has arrived
        chunk = sock.recv(
            64
        )  # => reads whatever is available, up to 64 bytes at a time
        if (
            not chunk
        ):  # => co-07: the client closed -- signal it upward as an empty line
            return b""  # => an EMPTY line signals "peer closed" up to the caller
        buffer.extend(chunk)  # => accumulate bytes across possibly many small reads
    line, _, rest = buffer.partition(
        b"\n"
    )  # => split off exactly one command, keep the remainder
    buffer[:] = (
        rest  # => whatever came AFTER the newline stays buffered for the NEXT command
    )
    return bytes(
        line
    )  # => bytearray.partition returns bytearray -- normalize to plain bytes


def handle_command(
    command: bytes,
) -> bytes:  # => co-01: the same PING/TIME protocol throughout
    if command == b"PING":  # => the simplest possible liveness check
        return b"PONG"  # => a FIXED reply -- the same for every PING, unlike TIME below
    if command == b"TIME":  # => a command that returns SERVER-side state, not an echo
        return str(int(time.time())).encode()  # => Unix epoch seconds, as ASCII digits
    return (
        b"ERR unknown command: " + command
    )  # => a graceful, protocol-level error reply


def handle_client(
    conn: socket.socket, addr: tuple[str, int]
) -> None:  # => co-10: one per client
    with conn:  # => this handler's own connection -- closes automatically on block exit
        buf = (
            bytearray()
        )  # => this client's own leftover-bytes buffer, private to its thread
        while True:  # => co-07: keeps serving commands until the client disconnects
            command = read_line(conn, buf)  # => reads ONE command line at a time
            if (
                not command
            ):  # => co-07: an empty line means the peer closed -- exit gracefully
                break  # => exits the loop -- the "with conn" block then closes gracefully
            conn.sendall(
                handle_command(command) + b"\n"
            )  # => reply, then wait for the next
    print(
        f"connection from {addr} closed gracefully"
    )  # => runs AFTER the "with" block's close()


def run_server(
    client_count: int,
) -> None:  # => co-10: serves exactly client_count connections
    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as sock:  # => same triple as Ex 29+
        sock.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )  # => same boilerplate as before
        sock.bind((HOST, PORT))  # => claims (HOST, PORT) for this process
        sock.listen(
            5
        )  # => backlog large enough for multiple clients to queue if needed
        print(
            f"listening on {HOST}:{PORT}", flush=True
        )  # => the signal a caller can wait for
        handlers: list[
            threading.Thread
        ] = []  # => one thread PER accepted connection (co-10)
        for _ in range(
            client_count
        ):  # => accepts exactly client_count clients, then stops
            conn, addr = (
                sock.accept()
            )  # => accept() itself is still sequential, one at a time
            handler = threading.Thread(
                target=handle_client, args=(conn, addr)
            )  # => co-10: unstarted
            handler.start()  # => handling happens CONCURRENTLY once each thread starts
            handlers.append(
                handler
            )  # => tracked so the loop below can wait for every one
        for (
            handler
        ) in handlers:  # => waits for EVERY handler thread, not just the last started
            handler.join()  # => waits for every spawned handler thread to finish


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    run_server(
        client_count=2
    )  # => this demo serves exactly two concurrent clients, then exits
