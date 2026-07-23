# learning/code/ex-24-so-reuseaddr-restart/so_reuseaddr_restart.py
"""Example 24: SO_REUSEADDR -- Rebinding a Port Still in TIME-WAIT."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import socket  # => co-11: SO_REUSEADDR is a raw socket option -- set with setsockopt() before bind(), not after
import threading  # => co-07: a real client connection is needed to put the server's port into TIME-WAIT at all
import time  # => co-07: small sleeps sequence the handshake/close so the server closes FIRST, deterministically

HOST = "127.0.0.1"  # => co-11: loopback -- the OS's own TIME-WAIT bookkeeping still applies here


def put_port_into_time_wait(port: int) -> None:  # => co-07: establishes a real connection, then closes the SERVER side first
    """Open a real connection to `port` and close it from the SERVER side -- leaving that port in TIME-WAIT."""  # => co-07: documents put_port_into_time_wait's contract -- no runtime output, just sets its __doc__
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-07: a temporary listener, only to accept ONE connection
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => co-11: needed for THIS setup bind only -- the real test is the rebind below
    server.bind((HOST, port))  # => co-07: binds the exact port this whole example will later try to rebind
    server.listen(1)  # => co-07: ready to accept the client thread's connection below

    def connect_and_close() -> None:  # => co-07: the CLIENT side -- connects, waits, then closes AFTER the server does
        time.sleep(0.1)  # => co-07: gives the server's accept() below time to be waiting first
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-07: a plain client socket, no special options needed
        client.connect((HOST, port))  # => co-07: a REAL three-way handshake -- co-07's TCP connection setup, exercised here
        time.sleep(0.3)  # => co-07: stays open until well after the server has closed its own side (see below)
        client.close()  # => co-07: the client closes LAST -- irrelevant to which side lands in TIME-WAIT

    client_thread = threading.Thread(target=connect_and_close)  # => co-07: runs the client concurrently with the server's accept()
    client_thread.start()  # => co-07: starts the client's connect/sleep/close sequence in the background
    conn, _ = server.accept()  # => co-07: blocks until the client thread's connect() above completes the handshake
    time.sleep(0.05)  # => co-07: a brief pause so the connection is genuinely established before this side closes it
    conn.close()  # => co-11: THE SERVER closes its side FIRST -- whichever side sends the first FIN lands in TIME-WAIT
    client_thread.join()  # => co-07: waits for the client thread's own (later) close to finish
    server.close()  # => co-07: releases the listening socket -- the PORT itself is now the one left in TIME-WAIT


if __name__ == "__main__":  # => co-11: entry point -- this block runs only when the file executes directly, not on import
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-11: a throwaway socket -- used only to claim a free ephemeral port
    probe.bind((HOST, 0))  # => co-11: port 0 -- let the OS pick a free port, avoiding a hardcoded, possibly-taken one
    port = probe.getsockname()[1]  # => co-11: remember the OS-assigned port -- every bind below targets this SAME port
    probe.close()  # => co-11: releases the throwaway socket immediately

    put_port_into_time_wait(port)  # => co-07: leaves `port` in a genuine TIME-WAIT state -- not simulated, actually triggered
    print(f"port {port} closed server-side first -- now lingering in TIME-WAIT")  # => co-11: confirms the setup step completed

    no_reuseaddr_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-11: a fresh socket, SO_REUSEADDR left at its OS default
    try:  # => co-11: WITHOUT SO_REUSEADDR, binding to a TIME-WAIT port is expected to fail
        no_reuseaddr_server.bind((HOST, port))  # => co-11: attempts to bind the SAME port that's still in TIME-WAIT
        print("bind WITHOUT SO_REUSEADDR: unexpectedly succeeded")  # => co-11: would only print if TIME-WAIT had already expired
        no_reuseaddr_server.close()  # => co-11: releases the socket in this unexpected-success branch
        without_reuseaddr_failed = False  # => co-11: records that no failure occurred, for the final assert below
    except OSError as exc:  # => co-11: "Address already in use" surfaces as an OSError -- this IS the expected outcome
        print(f"bind WITHOUT SO_REUSEADDR: failed as expected -- {exc}")  # => co-11: the exact OS error text, captured live
        no_reuseaddr_server.close()  # => co-11: releases the failed socket object
        without_reuseaddr_failed = True  # => co-11: records the expected failure, for the final assert below

    with_reuseaddr_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-11: a fresh socket -- SO_REUSEADDR set THIS time
    with_reuseaddr_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => co-11: THE one line this example demonstrates
    with_reuseaddr_server.bind((HOST, port))  # => co-11: binds the SAME still-in-TIME-WAIT port -- expected to succeed THIS time
    print(f"bind WITH SO_REUSEADDR on port {port}: succeeded immediately, no delay needed")  # => co-11: confirms the fix worked
    with_reuseaddr_server.listen(1)  # => co-11: proves the socket is fully usable, not merely bound
    with_reuseaddr_server.close()  # => co-11: releases the socket, cleaning up after the demonstration

    assert without_reuseaddr_failed, "binding a TIME-WAIT port WITHOUT SO_REUSEADDR must fail on this platform"  # => co-11
    print("SO_REUSEADDR let an immediate rebind succeed on a port still in TIME-WAIT: True")  # => co-11: both steps confirmed
    # => co-11: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
