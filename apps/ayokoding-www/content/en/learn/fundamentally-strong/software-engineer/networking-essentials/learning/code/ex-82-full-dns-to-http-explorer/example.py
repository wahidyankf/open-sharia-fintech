"""Example 82: A Full DNS -> TCP -> HTTP Explorer, with a UDP Contrast Note."""  # => co-12 capstone

import socket  # => stdlib sockets -- both the TCP and HTTP stages below live in this one module
import subprocess  # => co-20: shells out to the real `dig` binary, an independent resolver
import time  # => perf_counter() is what turns the TCP stage into a real, comparable number

HOST = "example.com"  # => co-01: the same demo host resolved throughout this topic
PORT = 80  # => co-05: HTTP's well-known port
PATH = "/"  # => co-02: the simplest possible request path


def dig_short(
    host: str,
) -> str:  # => co-20: shell out to `dig` for a real, tool-verified answer
    result = subprocess.run(  # => co-20: an EXTERNAL process, independent of Python's own resolver
        ["dig", "+short", host], capture_output=True, text=True, timeout=5, check=True
    )  # => args
    return result.stdout.strip().splitlines()[0]  # => the FIRST A record dig reports


def explore(
    host: str, port: int, path: str
) -> None:  # => narrates every layer as it happens
    print(
        f"=== resolving {host} ==="
    )  # => marks the START of the DNS stage in the transcript
    dig_ip = dig_short(host)  # => Stage 1a: an EXTERNAL tool's independent answer
    print(
        f"[dig]      {host} -> {dig_ip}"
    )  # => the external tool's own independent result
    python_ip = socket.gethostbyname(
        host
    )  # => Stage 1b: Python's OWN resolver call (co-03)
    print(
        f"[gethostbyname] {host} -> {python_ip}"
    )  # => Python's own result, for comparison

    print(
        f"=== opening a TCP connection to {python_ip}:{port} ==="
    )  # => marks the TCP stage start
    tcp_start = (
        time.perf_counter()
    )  # => a clock reading taken right before the TCP handshake
    sock = socket.create_connection(
        (python_ip, port), timeout=5
    )  # => Stage 2: co-07 handshake
    tcp_ms = (
        time.perf_counter() - tcp_start
    ) * 1000  # => convert seconds to milliseconds
    print(
        f"[TCP]      connected in {tcp_ms:.1f} ms"
    )  # => this stage's own isolated timing

    print(
        f"=== issuing GET {path} over that connection ==="
    )  # => marks the HTTP stage start
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"  # => co-12: by hand
    sock.sendall(request.encode("ascii"))  # => Stage 3: co-12
    response = (
        b""  # => accumulates the full response -- its final size isn't known in advance
    )
    while (
        True
    ):  # => co-11: loop until the server closes (Connection: close makes this safe)
        chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
        if not chunk:  # => an empty recv() means the server closed its side
            break  # => exits the while loop -- the full response has now been fully read
        response += (
            chunk  # => appends this chunk -- the loop above may run several times
        )
    sock.close()  # => releases the socket once the full response has been read
    status_line = response.split(b"\r\n", 1)[
        0
    ].decode()  # => co-13: the FIRST line, only
    print(
        f"[HTTP]     {status_line}"
    )  # => the final stage's own result, closing the DNS-to-HTTP chain

    print(
        "=== UDP contrast (co-08, co-09) ==="
    )  # => marks the closing prose note's start
    udp_note = (  # => co-08/co-09: a closing PROSE note, not a re-executed UDP request in this script
        "The DNS lookup above almost certainly traveled over UDP (dig's own transport, not"  # => co-08
        " shown on the wire here) -- a single connectionless query/response datagram, no"  # => co-09
        " handshake. Had it been dropped, dig would simply retry or time out; nothing"  # => text
        " resembling the TCP handshake or the ordered HTTP byte stream above would apply."
    )  # => end
    print(
        udp_note
    )  # => the note itself, tying the DNS stage back to co-08's UDP behavior


explore(HOST, PORT, PATH)  # => runs every stage, DNS through HTTP, on one real request
print(
    "ex-82 OK"
)  # => confirms all four stages -- dig, gethostbyname, TCP, HTTP -- completed
