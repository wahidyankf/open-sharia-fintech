# learning/code/ex-25-nonblocking-socket-select/nonblocking_socket_select.py
"""Example 25: Nonblocking Sockets -- setblocking(False) Polled with select.select."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import select  # => co-11: select.select() is the classic readiness-polling primitive this example demonstrates
import socket  # => co-11: setblocking(False) is a raw socket mode -- changes behavior, not the protocol on the wire
import threading  # => co-11: a delayed writer, run concurrently, is what makes "not ready yet" observable at all
import time  # => co-11: the delay itself -- long enough that an immediate (blocking) read would have nothing to return

HOST = "127.0.0.1"  # => co-11: loopback -- nonblocking mode and select() both work identically here as on any TCP socket
WRITE_DELAY_SECONDS = 0.3  # => co-11: how long the writer waits before sending anything at all


def delayed_writer(port: int) -> None:  # => co-11: connects immediately, but sends data only AFTER a deliberate delay
    """Connect immediately, then send one message only after a deliberate delay."""  # => co-11: documents delayed_writer's contract -- no runtime output, just sets its __doc__
    time.sleep(0.05)  # => co-11: a small head start so the reader below is already polling before this connects
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-11: an ordinary BLOCKING client socket -- only the reader is nonblocking here
    client.connect((HOST, port))  # => co-11: connects right away -- the CONNECTION exists well before any DATA does
    time.sleep(WRITE_DELAY_SECONDS)  # => co-11: THE deliberate gap -- during this window, a blocking recv() would just hang
    client.sendall(b"finally ready")  # => co-11: only now does data actually arrive for the reader to observe
    client.close()  # => co-11: releases this connection's resources on the writer side


if __name__ == "__main__":  # => co-11: entry point -- this block runs only when the file executes directly, not on import
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-11: the listening socket the nonblocking reader will accept on
    server_sock.bind((HOST, 0))  # => co-11: port 0 -- let the OS pick a free ephemeral port
    server_sock.listen(1)  # => co-11: one pending connection is all this single-client demo needs
    port = server_sock.getsockname()[1]  # => co-11: the OS-assigned port, needed by the delayed writer thread to connect back

    writer_thread = threading.Thread(target=delayed_writer, args=(port,))  # => co-11: runs delayed_writer() concurrently
    writer_thread.start()  # => co-11: starts the connect-then-delay-then-send sequence in the background

    conn, _ = server_sock.accept()  # => co-11: this accept() is still BLOCKING -- only the data-read path below is nonblocking
    conn.setblocking(False)  # => co-11: THE line this example is about -- recv() now raises instead of blocking when no data is ready

    poll_count = 0  # => co-11: how many times select() reported "not ready yet" before data finally arrived
    data = b""  # => co-11: accumulates the eventually-received bytes
    start = time.monotonic()  # => co-11: wall-clock start, to report how long the polling loop actually ran
    while not data:  # => co-11: keep polling until SOMETHING has been read
        readable, _, _ = select.select([conn], [], [], 0.05)  # => co-11: waits UP TO 0.05s for `conn` to become readable, then returns
        if conn in readable:  # => co-11: select() says data (or EOF) is now available -- safe to recv() without blocking
            data = conn.recv(1024)  # => co-11: nonblocking recv() -- guaranteed not to block, since select() just confirmed readiness
        else:  # => co-11: select()'s timeout elapsed with nothing ready -- exactly the "would have blocked" case
            poll_count += 1  # => co-11: counts this as one confirmed "not ready yet" observation
    elapsed = time.monotonic() - start  # => co-11: total time spent polling before data finally arrived

    print(f"polled {poll_count} times before data was ready (elapsed {elapsed:.2f}s)")  # => co-11: the polling-loop summary
    print(f"received: {data!r}")  # => co-11: the eventually-received payload, once select() confirmed readiness
    conn.close()  # => co-11: releases this connection's resources on the reader side
    server_sock.close()  # => co-11: releases the listening socket
    writer_thread.join()  # => co-11: waits for the writer thread to finish its connect/delay/send sequence

    assert poll_count >= 1, "select() must have reported 'not ready' at least once before data arrived"  # => co-11
    assert data == b"finally ready", "the eventually-received payload must match exactly what the writer sent"  # => co-11
    print("select() correctly polled a nonblocking socket instead of hanging on an unready read: True")  # => co-11
    # => co-11: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
