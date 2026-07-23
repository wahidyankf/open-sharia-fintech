# learning/code/ex-23-tcp-nodelay-socket-option/tcp_nodelay_socket_option.py
"""Example 23: TCP_NODELAY -- Measuring the Nagle/Delayed-ACK Stall."""  # => co-10, co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import socket  # => co-11: TCP_NODELAY (co-11) is a raw socket option -- only visible below the application layer
import statistics  # => co-11: mean() over several trials, so one lucky/unlucky run doesn't skew the reported comparison
import threading  # => co-10: runs the server concurrently with the client on one localhost connection
import time  # => co-10: monotonic() timestamps around each round trip -- what actually reveals Nagle's stall

HOST = "127.0.0.1"  # => co-10: loopback -- the kernel's REAL TCP stack still applies Nagle/delayed-ACK here
ITERATIONS = 20  # => co-10: enough round trips for statistics.mean() to smooth out any single-trial noise


def server(server_sock: socket.socket, iterations: int) -> None:  # => co-10: waits for the FULL 2-byte message before replying
    """Accept one connection; for each iteration, wait for 2 bytes, then reply with 1 ack byte."""  # => co-10: documents server's contract -- no runtime output, just sets its __doc__
    conn, _ = server_sock.accept()  # => co-10: blocks here until the client below connects
    for _ in range(iterations):  # => co-10: one accumulate-then-reply cycle per round trip
        received = b""  # => co-10: accumulates bytes across possibly-separate recv() calls
        while len(received) < 2:  # => co-10: keep reading until BOTH of the client's split writes have arrived
            received += conn.recv(2 - len(received))  # => co-10: never over-reads past this iteration's 2-byte message
        conn.sendall(b"K")  # => co-10: only NOW does the server reply -- nothing to piggyback an early ACK on before this
    conn.close()  # => co-10: releases this connection's resources on the server side


def measure_round_trips(nodelay: bool, iterations: int) -> list[float]:  # => co-11: runs one full trial, Nagle on or off
    """Run `iterations` split-write round trips with TCP_NODELAY either set or left at its default (Nagle-enabled)."""  # => co-11: documents measure_round_trips's contract -- no runtime output, just sets its __doc__
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-10: a fresh listening socket per trial -- no state carries over
    server_sock.bind((HOST, 0))  # => co-10: port 0 -- let the OS pick a free ephemeral port
    server_sock.listen(1)  # => co-10: one pending connection is all this single-client demo needs
    port = server_sock.getsockname()[1]  # => co-10: the OS-assigned port, needed by the client below to connect back
    server_thread = threading.Thread(target=server, args=(server_sock, iterations))  # => co-10: runs server() concurrently
    server_thread.start()  # => co-10: starts accepting in the background

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-11: the CLIENT side -- the socket TCP_NODELAY is set on
    if nodelay:  # => co-11: the ONLY difference between the two trials this function is called with
        client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # => co-11: disables Nagle -- flush every write immediately
    client_sock.connect((HOST, port))  # => co-11: connects to the server's listening port

    latencies_ms: list[float] = []  # => co-10: one measured round-trip time per iteration, in milliseconds
    for _ in range(iterations):  # => co-10: repeat the split-write round trip ITERATIONS times
        start = time.monotonic()  # => co-10: timestamp taken right before the first of the two split writes
        client_sock.send(b"H")  # => co-10: FIRST small write -- with Nagle enabled, this segment goes out immediately (no data in flight yet)
        client_sock.send(b"I")  # => co-10: SECOND small write, sent RIGHT AFTER -- Nagle withholds this one until the first is ACKed
        client_sock.recv(1)  # => co-10: blocks until the server's 1-byte reply arrives -- completing this iteration's round trip
        latencies_ms.append((time.monotonic() - start) * 1000)  # => co-10: elapsed time for this ENTIRE round trip, in ms
    client_sock.close()  # => co-11: releases this connection's resources on the client side
    server_thread.join()  # => co-10: waits for the server thread to finish its iterations loop
    server_sock.close()  # => co-10: releases the listening socket
    return latencies_ms  # => co-10: returns this computed value to the caller


if __name__ == "__main__":  # => co-11: entry point -- this block runs only when the file executes directly, not on import
    nagle_latencies = measure_round_trips(nodelay=False, iterations=ITERATIONS)  # => co-10: DEFAULT socket -- Nagle enabled
    nodelay_latencies = measure_round_trips(nodelay=True, iterations=ITERATIONS)  # => co-11: TCP_NODELAY set -- Nagle disabled
    nagle_mean = statistics.mean(nagle_latencies)  # => co-10: average round trip WITH Nagle -- expect it inflated by the stall
    nodelay_mean = statistics.mean(nodelay_latencies)  # => co-11: average round trip WITHOUT Nagle -- expect near-zero overhead
    print(f"Nagle (default)   mean round trip = {nagle_mean:.2f} ms  (samples: {[round(x, 1) for x in nagle_latencies[:5]]}...)")  # => co-10
    print(f"TCP_NODELAY       mean round trip = {nodelay_mean:.2f} ms  (samples: {[round(x, 1) for x in nodelay_latencies[:5]]}...)")  # => co-11
    assert nodelay_mean < nagle_mean, "TCP_NODELAY's mean round trip must be lower than Nagle's default mean"  # => co-11: the headline claim
    speedup = nagle_mean / nodelay_mean if nodelay_mean > 0 else float("inf")  # => co-10: how many times faster NODELAY was, on average
    print(f"TCP_NODELAY was ~{speedup:.0f}x faster on this split-write round trip: True")  # => co-11: reached only if the assert passed
    # => co-11: this file is self-verifying: if it exits 0, the assert above passed and the demonstrated claim held
