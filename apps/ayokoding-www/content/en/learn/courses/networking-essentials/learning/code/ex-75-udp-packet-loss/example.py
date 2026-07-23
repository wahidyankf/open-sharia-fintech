"""Example 75: UDP Packet Loss -- Genuinely Overflowing a Receive Buffer."""

import socket  # => stdlib sockets -- SO_RCVBUF below is the whole mechanism this example turns on
import threading  # => runs the tiny-buffered server concurrently with the fast-firing sender
import time  # => only a brief startup head start, not real measurement

HOST = "127.0.0.1"  # => loopback -- keeps this packet-loss demo local and deterministic
PORT = 50075  # => co-05: a fresh ephemeral port, unique to this example
DATAGRAM_COUNT = 2000  # => far more datagrams than the deliberately tiny receive buffer can hold  # fmt: skip


def run_server(result: dict[str, int]) -> None:  # => "result" is how the count escapes this thread  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # => co-08: UDP, not TCP  # fmt: skip
        # A deliberately TINY receive buffer (co-08): once the kernel's queue for this socket
        # fills up, the OS silently DROPS any further arriving datagrams -- no error, no
        # retransmission, exactly the "delivery is not guaranteed" behavior RFC 768 describes.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2048)  # => the deliberately tiny buffer  # fmt: skip
        sock.bind((HOST, PORT))  # => UDP: binds, but never listen()s or accept()s at all  # fmt: skip
        sock.settimeout(1.0)  # => stop reading once the sender has clearly finished
        received = 0  # => counts only datagrams that ACTUALLY arrived, not ones that were sent  # fmt: skip
        try:  # => wrapped because the timeout above is EXPECTED to fire once sending stops
            while True:  # => co-11: keeps reading until no more datagrams arrive within 1 second  # fmt: skip
                sock.recvfrom(64)  # => each call surfaces one datagram, if the buffer still has one  # fmt: skip
                received += 1  # => incremented once per datagram that genuinely made it through  # fmt: skip
        except TimeoutError:
            pass  # => no more datagrams arriving -- the sender is done
        result["received"] = received  # => the final tally, handed back to the main thread  # fmt: skip


result: dict[str, int] = {}  # => co-01: measured, not assumed, exactly like Example 24 did  # fmt: skip
server_thread = threading.Thread(target=run_server, args=(result,), daemon=True)
server_thread.start()  # => the tiny-buffered receiver begins running concurrently
time.sleep(0.1)  # => a brief head start so the server's tiny-buffered socket is bound and ready  # fmt: skip

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # => the sender's own UDP socket  # fmt: skip
    for i in range(DATAGRAM_COUNT):  # => co-08: fired as fast as possible, NO waiting for acks  # fmt: skip
        sock.sendto(f"packet-{i}".encode(), (HOST, PORT))  # => sendto never blocks on the buffer  # fmt: skip

server_thread.join(timeout=5)  # => waits for the server's 1-second post-burst timeout to fire  # fmt: skip

received = result["received"]  # => the ACTUAL count of datagrams that survived the tiny buffer  # fmt: skip
dropped = DATAGRAM_COUNT - received  # => everything sent but never received -- genuine loss  # fmt: skip
print(f"sent {DATAGRAM_COUNT} datagrams, server received {received}, {dropped} were dropped")  # fmt: skip

# The EXACT drop count varies run to run (kernel scheduling, buffer timing) -- what's
# guaranteed is that AT LEAST some were dropped, since 2000 datagrams into a 2048-byte
# buffer cannot all fit, and UDP performs no retransmission to recover the rest (co-08, co-09).
assert received < DATAGRAM_COUNT  # => confirms genuine, observed loss occurred this run
assert received > 0  # => confirms it wasn't a total, unrelated failure either
print("ex-75 OK")  # => confirms the loss was genuinely observed, neither total nor zero
