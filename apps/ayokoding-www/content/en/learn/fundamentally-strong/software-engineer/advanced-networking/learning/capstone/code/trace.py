# learning/capstone/code/trace.py
"""Capstone Step 2: trace.py -- an annotated DNS -> TCP -> TLS -> HTTP timeline for one real request.

Ties together co-01 (the layered model applied to a real packet), co-07 (the TCP handshake), and
co-14 (the TLS 1.3 handshake) into one script: resolves a real host, times each stage separately,
and narrates all four layers a `curl -v` transcript (Examples 1 and 30) shows more implicitly.
"""  # => co-01: this file's own restated purpose, doubling as its module __doc__
# => co-01: no runtime output beyond setting __doc__ -- the three paragraphs above just orient the reader

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import socket  # => co-01: getaddrinfo (DNS) and create_connection (TCP) -- both stdlib, both real network calls
import ssl  # => co-14: wraps a plain TCP socket in a genuine TLS 1.3 handshake, stdlib-only
import time  # => co-01: perf_counter -- a monotonic, high-resolution clock, the right tool for timing each stage

HOST = "example.com"  # => co-01: RFC 2606-reserved for documentation -- the same host Examples 1 and 30 used
PORT = 443  # => co-01: HTTPS's well-known port (Example 16's ports table)


def resolve(host: str, port: int) -> tuple[str, float]:  # => co-01: STAGE 1 -- DNS, the Application-layer name lookup every request starts with
    """Resolve `host` to an IPv4/IPv6 address, returning (address, elapsed_seconds)."""  # => co-01: documents resolve's contract -- no runtime output, just sets its __doc__
    start = time.perf_counter()  # => co-01: timestamp taken right before the resolution call
    address_info = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)  # => co-01: a REAL DNS lookup -- no mock, no cache bypass trick
    elapsed = time.perf_counter() - start  # => co-01: how long resolution itself took, isolated from every later stage
    resolved_ip = str(address_info[0][4][0])  # => co-01: the first returned address -- exactly what a plain socket.connect would also pick; str() satisfies strict typing, since getaddrinfo's sockaddr element type is a union
    return resolved_ip, elapsed  # => co-01: returns this computed value to the caller


def connect_tcp(ip: str, port: int) -> tuple[socket.socket, float]:  # => co-07: STAGE 2 -- the TCP three-way handshake (co-07), Transport layer
    """Open a real TCP connection to (ip, port), returning (socket, elapsed_seconds)."""  # => co-07: documents connect_tcp's contract -- no runtime output, just sets its __doc__
    start = time.perf_counter()  # => co-07: timestamp taken right before the connect call
    sock = socket.create_connection((ip, port), timeout=5)  # => co-07: a REAL SYN/SYN-ACK/ACK handshake against the resolved IP -- this call blocks until it completes
    elapsed = time.perf_counter() - start  # => co-07: how long the handshake itself took, isolated from DNS and TLS
    return sock, elapsed  # => co-07: returns this computed value to the caller


def handshake_tls(sock: socket.socket, server_hostname: str) -> tuple[ssl.SSLSocket, float]:  # => co-14: STAGE 3 -- TLS 1.3's 1-RTT handshake (co-14), sits between Transport and Application
    """Wrap `sock` in a real TLS handshake, returning (tls_socket, elapsed_seconds)."""  # => co-14: documents handshake_tls's contract -- no runtime output, just sets its __doc__
    context = ssl.create_default_context()  # => co-14: the stdlib's OWN certificate-validation policy -- no shortcuts, a real chain-of-trust check
    start = time.perf_counter()  # => co-14: timestamp taken right before the handshake call
    tls_sock = context.wrap_socket(sock, server_hostname=server_hostname)  # => co-14: a REAL TLS 1.3 handshake -- ClientHello+KeyShare through Finished, exactly Example 31's diagram
    elapsed = time.perf_counter() - start  # => co-14: how long the handshake itself took, isolated from DNS and TCP
    return tls_sock, elapsed  # => co-14: returns this computed value to the caller


def send_http_request(tls_sock: ssl.SSLSocket, host: str) -> tuple[str, float]:  # => co-01: STAGE 4 -- HTTP, back at the Application layer, now riding the encrypted TLS channel
    """Send a minimal HTTP/1.1 GET and return (status_line, elapsed_seconds)."""  # => co-01: documents send_http_request's contract -- no runtime output, just sets its __doc__
    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode()  # => co-01: the literal wire bytes of an HTTP/1.1 request -- Example 1's exact request shape
    start = time.perf_counter()  # => co-01: timestamp taken right before the request is sent
    tls_sock.sendall(request)  # => co-01: writes the request onto the ALREADY-ENCRYPTED TLS channel from stage 3
    response = b""  # => co-01: accumulates bytes across possibly-separate recv() calls
    while b"\r\n\r\n" not in response:  # => co-01: reads only until the header block's terminating blank line -- the body isn't needed for this timeline
        chunk = tls_sock.recv(4096)  # => co-01: reads whatever arrives next -- HTTP responses are not guaranteed to land in one recv() call
        if not chunk:  # => co-01: an empty recv() would mean the peer closed early, before any full header block arrived
            break  # => co-01: stops the loop rather than spinning on a closed connection
        response += chunk  # => co-01: appends this chunk to the running buffer
    elapsed = time.perf_counter() - start  # => co-01: how long the request/response round trip itself took
    status_line = response.split(b"\r\n", 1)[0].decode()  # => co-01: the first line -- e.g. "HTTP/1.1 200 OK", Example 1's own status line
    return status_line, elapsed  # => co-01: returns this computed value to the caller


if __name__ == "__main__":  # => co-01: entry point -- this block runs only when the file executes directly, not on import
    overall_start = time.perf_counter()  # => co-01: the whole-timeline clock, spanning all four stages
    ip, dns_seconds = resolve(HOST, PORT)  # => co-01: STAGE 1 -- DNS
    print(f"[DNS]  resolved {HOST} -> {ip} in {dns_seconds * 1000:.1f} ms")  # => co-01: labels this stage explicitly with its OSI/TCP-IP layer name

    tcp_sock, tcp_seconds = connect_tcp(ip, PORT)  # => co-07: STAGE 2 -- TCP
    print(f"[TCP]  three-way handshake to {ip}:{PORT} completed in {tcp_seconds * 1000:.1f} ms")  # => co-07: labels this stage explicitly with its layer name

    tls_sock, tls_seconds = handshake_tls(tcp_sock, HOST)  # => co-14: STAGE 3 -- TLS
    negotiated_version = tls_sock.version()  # => co-14: e.g. "TLSv1.3" -- confirms which protocol version was actually negotiated
    cipher_info = tls_sock.cipher()  # => co-14: returns None if no cipher was negotiated -- checked explicitly below for strict typing
    assert cipher_info is not None, "a completed TLS handshake must have negotiated a cipher suite"  # => co-14: narrows cipher_info from Optional to a concrete tuple for the line below
    negotiated_cipher = cipher_info[0]  # => co-14: e.g. "TLS_AES_256_GCM_SHA384" -- the negotiated AEAD cipher suite
    print(f"[TLS]  handshake complete -- {negotiated_version} / {negotiated_cipher} in {tls_seconds * 1000:.1f} ms")  # => co-14: labels this stage AND names what was negotiated

    status_line, http_seconds = send_http_request(tls_sock, HOST)  # => co-01: STAGE 4 -- HTTP
    print(f"[HTTP] {status_line} in {http_seconds * 1000:.1f} ms")  # => co-01: labels this final stage with its own layer name and the real response status line

    total_seconds = time.perf_counter() - overall_start  # => co-01: the full DNS-to-HTTP timeline, end to end
    print(f"\ntotal: {total_seconds * 1000:.1f} ms across all four stages")  # => co-01: the capstone's own headline summary number
    tls_sock.close()  # => co-14: releases this connection's resources -- closes the TLS layer, which also closes the underlying TCP socket

    assert status_line.startswith("HTTP/1.1 "), "the response must carry a real HTTP/1.1 status line"  # => co-01: the acceptance criterion this step's syllabus entry (ex-trace) names
    assert negotiated_version == "TLSv1.3", "example.com is expected to negotiate TLS 1.3, per this topic's Example 30"  # => co-14
    assert dns_seconds > 0 and tcp_seconds > 0 and tls_seconds > 0 and http_seconds > 0, "every stage must take a measurable, nonzero amount of time"  # => co-01
    print("All four stages (DNS, TCP, TLS, HTTP) measured and narrated against a real live request: True")  # => co-01: reached only if every assert above passed
    # => co-01: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
    # => co-01: each stage function returns its OWN isolated elapsed time -- summing them individually (not just timing start-to-finish) is what makes the per-stage breakdown trustworthy
