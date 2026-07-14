"""Example 57: TCP vs. UDP -- the Same Message, Two Different APIs."""

import socket  # => stdlib sockets -- both TCP and UDP go through this one module
import threading  # => runs BOTH server variants concurrently, side by side

HOST = "127.0.0.1"  # => loopback -- keeps this contrast demo local and deterministic
TCP_PORT = 50057  # => co-05: TCP and UDP need SEPARATE ports even on the same host
UDP_PORT = 50157  # => a different port from TCP_PORT -- the two protocols don't share a namespace


def tcp_server(ready: threading.Event) -> None:  # => co-07: connection-oriented, byte-stream  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => same boilerplate as before  # fmt: skip
        sock.bind((HOST, TCP_PORT))  # => claims the TCP port -- UDP claims its OWN port below  # fmt: skip
        sock.listen(1)  # => TCP-only: listen() marks the socket passive
        ready.set()
        conn, _ = sock.accept()  # => TCP-only: an explicit three-way-handshake accept step  # fmt: skip
        with conn:  # => TCP-only: accept() hands back a SEPARATE connected socket from "sock"  # fmt: skip
            for _ in range(3):  # => the client sends exactly three messages over one connection  # fmt: skip
                data = conn.recv(64)  # => reads from the connected "conn", not the listening "sock"  # fmt: skip
                conn.sendall(data)  # => echoes on the same persistent connection, no re-addressing  # fmt: skip


def udp_server(ready: threading.Event) -> None:  # => co-08: connectionless, message-oriented  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # => SOCK_DGRAM, not SOCK_STREAM  # fmt: skip
        sock.bind((HOST, UDP_PORT))  # => UDP: binds, but never listen()s or accept()s at all  # fmt: skip
        ready.set()
        for _ in range(3):  # => the client sends exactly three independent datagrams
            data, addr = sock.recvfrom(64)  # => each call surfaces the sender's address directly  # fmt: skip
            sock.sendto(data, addr)  # => UDP-only: every reply re-addresses explicitly, no "conn"  # fmt: skip


tcp_ready = threading.Event()  # => a separate ready-signal per server, since two servers now race  # fmt: skip
udp_ready = threading.Event()  # => set independently once udp_server's own bind() completes  # fmt: skip
threading.Thread(target=tcp_server, args=(tcp_ready,), daemon=True).start()
# => starts the TCP server concurrently with the UDP server line right below
threading.Thread(target=udp_server, args=(udp_ready,), daemon=True).start()
# => both servers now run side by side -- neither blocks the other from starting
tcp_ready.wait(timeout=5)  # => blocks until the TCP server's own bind()+listen() truly completed  # fmt: skip
udp_ready.wait(timeout=5)  # => blocks until the UDP server's own bind() truly completed

# TCP: ONE connect() call, then a persistent stream -- order is guaranteed (co-07).
tcp_replies: list[bytes] = []
with socket.create_connection((HOST, TCP_PORT), timeout=5) as sock:  # => the explicit handshake  # fmt: skip
    for msg in (b"one", b"two", b"three"):  # => all three ride the SAME already-open connection  # fmt: skip
        sock.sendall(msg)  # => no destination argument needed -- connect() already fixed the peer  # fmt: skip
        tcp_replies.append(sock.recv(64))  # => recv() carries no sender info -- there's one peer  # fmt: skip
print(f"TCP replies (order guaranteed): {tcp_replies}")

# UDP: NO connect() call -- every send is independently addressed (co-08).
udp_replies: list[bytes] = []
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # => a plain, unconnected UDP socket  # fmt: skip
    sock.settimeout(5)  # => co-08: no delivery guarantee, so a timeout avoids hanging forever  # fmt: skip
    for msg in (b"one", b"two", b"three"):  # => three separate, individually-addressed datagrams  # fmt: skip
        sock.sendto(msg, (HOST, UDP_PORT))  # => every datagram names its destination explicitly  # fmt: skip
        reply, _ = sock.recvfrom(64)  # => recvfrom() DOES surface sender info -- UDP has no "conn"  # fmt: skip
        udp_replies.append(reply)  # => appended in receive order, which UDP never itself promises  # fmt: skip
print(f"UDP replies (order NOT guaranteed by the protocol): {udp_replies}")

assert tcp_replies == [b"one", b"two", b"three"]  # => TCP: exact order, every time
assert set(udp_replies) == {b"one", b"two", b"three"}  # => UDP: all arrived, order not promised  # fmt: skip
# TCP asserts an exact LIST (order matters); UDP asserts only a SET (order does not) -- that
# single difference in the assertion itself is the API contrast this whole example demonstrates.
# On this machine's loopback interface both happen to arrive in order -- the API difference
# (connect/accept vs. bind-only, recv vs. recvfrom) is real regardless of what one run shows;
# Example 75 demonstrates UDP's lack of a delivery guarantee concretely, with real loss.
print("ex-57 OK")  # => confirms both API shapes completed their three-message exchange
