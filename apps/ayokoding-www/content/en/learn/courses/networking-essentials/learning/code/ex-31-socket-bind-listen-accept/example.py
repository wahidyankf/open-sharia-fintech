"""Example 31: socket.bind / .listen / .accept, Annotated."""

import socket  # => same stdlib module used by every server/client in this tier
import threading  # => used only for the ready-signal + background thread below, not real load

HOST = "127.0.0.1"  # => loopback -- no traffic ever leaves this machine
PORT = 50031  # => an unregistered ephemeral port (co-05)


def server(ready: threading.Event) -> None:  # => runs on a background thread (co-10)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => AF_INET+SOCK_STREAM = TCP  # fmt: skip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => allow instant re-bind  # fmt: skip
        sock.bind((HOST, PORT))  # => bind: CLAIMS this (address, port) pair for this process  # fmt: skip
        # => after bind, the socket has an address but is not yet accepting connections
        sock.listen(1)  # => listen: flips the socket into PASSIVE mode, backlog of 1 pending conn  # fmt: skip
        # => after listen, the OS will queue up to 1 incoming SYN before accept() is even called
        print("state: bound and listening")  # => Output line 1
        ready.set()  # => signals the main thread it is safe to connect now
        conn, addr = sock.accept()  # => accept: BLOCKS until a client completes the handshake  # fmt: skip
        # => accept() returns a NEW socket (conn) distinct from the listening socket (sock) --
        # => sock keeps listening for MORE clients; conn is this one client's private channel
        print(f"state: accepted a connection from {addr}")  # => Output line 2
        with conn:
            conn.recv(16)  # => drains whatever the client sent, so it can close cleanly


ready_event = threading.Event()  # => co-11: coordinates "server is ready" without a sleep guess  # fmt: skip
server_thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True means this thread never blocks process exit if something above hangs
server_thread.start()  # => starts the server concurrently with the code below
ready_event.wait(timeout=5)  # => blocks the main thread until bind()+listen() have both run  # fmt: skip

with socket.create_connection((HOST, PORT), timeout=5) as client_sock:  # => triggers accept() above  # fmt: skip
    client_sock.sendall(b"hi")  # => a few bytes so the server's recv() has something to drain  # fmt: skip
    print("state: client connected successfully")  # => Output line 3

server_thread.join(timeout=5)  # => waits for the server thread to finish handling that one client  # fmt: skip
print("ex-31 OK")  # => confirms the full bind/listen/accept sequence completed cleanly
