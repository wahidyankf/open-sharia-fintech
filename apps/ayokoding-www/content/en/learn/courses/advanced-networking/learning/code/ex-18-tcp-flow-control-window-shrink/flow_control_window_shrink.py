# learning/code/ex-18-tcp-flow-control-window-shrink/flow_control_window_shrink.py
"""Example 18: TCP Flow Control -- a Slow Reader Blocks a Fast Writer."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import socket  # => co-08: raw sockets -- the level flow control actually operates at, below any application framing
import threading  # => co-08: runs the SLOW reader concurrently with the fast writer on one localhost connection
import time  # => co-08: sleeps simulate a receiver that is busy/slow, and times the writer's blocking send() call

HOST = "127.0.0.1"  # => co-08: loopback -- no real network needed, only the kernel's OWN TCP stack on both ends
CHUNK = 65536  # => co-08: 64 KiB per send() call -- large enough to fill a shrunk window in only a few calls
SLOW_READ_DELAY_SECONDS = 2.0  # => co-08: how long the "slow reader" sleeps BEFORE its first recv() call
SEND_TIMEOUT_SECONDS = 1.0  # => co-08: how long the writer waits before treating a stalled send() as "blocked by the window"


def slow_reader(server_sock: socket.socket, received: list[int]) -> None:  # => co-08: the RECEIVER side -- deliberately withholds recv()
    """Accept one connection, sleep (simulating a busy receiver), then drain everything at once."""  # => co-08: documents slow_reader's contract -- no runtime output, just sets its __doc__
    conn, _ = server_sock.accept()  # => co-08: blocks here until the client (writer) below connects
    time.sleep(SLOW_READ_DELAY_SECONDS)  # => co-08: THE key delay -- no recv() calls happen while the sender is writing
    total = 0  # => co-08: running count of bytes eventually drained, once reading finally starts
    conn.settimeout(0.5)  # => co-08: bounds the final drain loop so this thread cannot hang forever
    try:  # => co-08: the drain loop below ends naturally once the writer stops sending (timeout) or closes
        while True:  # => co-08: keep draining until no more data arrives within the timeout window
            data = conn.recv(CHUNK)  # => co-08: NOW the receiver finally starts reading -- this is what un-shrinks the window
            if not data:  # => co-08: an empty recv() means the peer closed its write side (a FIN was received)
                break  # => co-08: nothing more will ever arrive -- stop draining
            total += len(data)  # => co-08: tally every byte actually read off the socket
    except TimeoutError:  # => co-08: no more data within 0.5s -- treat this as "the writer is done sending"
        pass  # => co-08: expected end-of-burst condition, not an error
    received.append(total)  # => co-08: reports the final drained byte count back to the main thread
    conn.close()  # => co-08: releases this connection's resources on the receiver side


if __name__ == "__main__":  # => co-08: entry point -- this block runs only when the file executes directly, not on import
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-08: the listening socket the slow reader accepts on
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)  # => co-08: request a SMALL receive buffer -- shrinks the window sooner
    server_sock.bind((HOST, 0))  # => co-08: port 0 -- let the OS pick a free ephemeral port, avoiding hardcoded-port collisions
    server_sock.listen(1)  # => co-08: one pending connection is all this single-client demo needs
    port = server_sock.getsockname()[1]  # => co-08: the OS-assigned port, needed by the client below to connect back

    received: list[int] = []  # => co-08: a mutable box the reader thread appends its final tally into, for the main thread to read
    reader_thread = threading.Thread(target=slow_reader, args=(server_sock, received))  # => co-08: runs slow_reader() concurrently
    reader_thread.start()  # => co-08: starts accepting (and then deliberately delaying) in the background

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-08: the WRITER side -- tries to send as fast as it can
    client_sock.connect((HOST, port))  # => co-08: connects to the slow reader's listening port
    client_sock.settimeout(SEND_TIMEOUT_SECONDS)  # => co-08: without this, a full send buffer would block FOREVER, not just slow down
    payload = b"x" * CHUNK  # => co-08: one 64 KiB chunk, reused on every send() call below

    sent_before_block = 0  # => co-08: total bytes the writer got out BEFORE flow control first stalled it
    blocked = False  # => co-08: True once a send() call actually times out -- the moment the window is confirmed full
    start = time.monotonic()  # => co-08: wall-clock start, so the eventual stall can be reported with a real elapsed time
    for attempt in range(1, 21):  # => co-08: up to 20 chunks (1.25 MiB) -- far more than a 4 KiB-buffered window can absorb unread
        try:  # => co-08: each send() either succeeds immediately or times out once the window is exhausted
            client_sock.sendall(payload)  # => co-08: sendall() loops internally until every byte is queued -- exactly where blocking shows up
            sent_before_block += CHUNK  # => co-08: this attempt's bytes made it into the socket's own send buffer
        except TimeoutError:  # => co-08: sendall() could not queue more bytes within SEND_TIMEOUT_SECONDS -- THIS is flow control
            blocked = True  # => co-08: the defining observation this example exists to demonstrate
            print(f"send() blocked on attempt {attempt} after {sent_before_block} bytes queued -- receiver's window is full")  # => co-08
            break  # => co-08: no need to keep retrying -- the claim is already demonstrated
    elapsed = time.monotonic() - start  # => co-08: how long the writer spent before flow control kicked in
    client_sock.close()  # => co-08: releases this connection's resources on the writer side -- also unblocks the slow reader's drain

    reader_thread.join()  # => co-08: waits for the reader thread to finish draining and record its tally
    server_sock.close()  # => co-08: releases the listening socket

    print(f"writer sent {sent_before_block} bytes before blocking (elapsed {elapsed:.2f}s)")  # => co-08: the writer-side summary
    print(f"reader eventually drained {received[0]} bytes total")  # => co-08: the receiver-side summary, once it finally read
    assert blocked, "a 4 KiB receive buffer with a 2s-delayed reader must eventually block a 64 KiB-chunk sender"  # => co-08
    assert sent_before_block > 0, "at least the first chunk must have been queued before any blocking occurred"  # => co-08
    print("Flow control demonstrably slowed/blocked the fast writer: True")  # => co-08: reached only if both asserts passed
    # => co-08: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
