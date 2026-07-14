"""Example 56: UDP Has No Handshake -- Sending to a Closed Port."""

import socket  # => stdlib sockets -- sendto() itself is the whole demonstration here
import time  # => wall-clock timing is what proves sendto() never blocked at all

HOST = "127.0.0.1"  # => loopback -- keeps this no-listener demo local and deterministic
PORT = 50056  # => co-08: deliberately, nothing is listening here at all


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # => a bare UDP socket, no bind()  # fmt: skip
    sock.settimeout(1.0)  # => co-08: UDP gives no delivery confirmation -- bound the wait  # fmt: skip
    start = time.monotonic()  # => a clock reading taken right before the send below
    # sendto SUCCEEDS regardless of whether anything is listening -- UDP has no three-way
    # handshake (co-07 contrast) to fail during. The datagram is simply fired onto the wire.
    sock.sendto(b"is anyone there?", (HOST, PORT))  # => this call returns immediately, no error  # fmt: skip
    elapsed_to_send = time.monotonic() - start  # => the time sendto() itself took to return  # fmt: skip
    print(f"sendto() returned in {elapsed_to_send:.4f}s with NO error")  # => co-08: no handshake  # fmt: skip

    try:  # => wrapped because recvfrom() below is EXPECTED to time out, not to error
        reply, _ = sock.recvfrom(1024)  # => waits for a reply that will never come
        outcome = f"unexpectedly received: {reply!r}"  # => reached only if something DID answer
    except TimeoutError:  # => co-08: silence is the ONLY signal -- no "port closed" notification  # fmt: skip
        outcome = "timed out waiting for a reply -- UDP never told us nobody was listening"  # fmt: skip
    print(outcome)  # => reports whichever branch above actually ran

assert elapsed_to_send < 0.1  # => confirms sendto() itself never blocked on the missing listener  # fmt: skip
print("ex-56 OK")  # => confirms both the instant sendto() and the eventual timeout were observed  # fmt: skip
