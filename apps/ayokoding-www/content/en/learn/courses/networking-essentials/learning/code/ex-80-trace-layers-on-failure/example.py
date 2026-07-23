"""Example 80: A DNS Failure and a TCP Failure Surface at DIFFERENT Layers."""

import socket  # => stdlib sockets -- both the DNS and TCP failure paths live in this one module

# .invalid is an RFC 2606-reserved TLD, GUARANTEED to never resolve -- unlike most
# "made up" domains, this one is contractually reserved to always fail DNS (co-03).
BAD_HOST = "this-host-does-not-exist-at-all.invalid"

# 127.0.0.1 always resolves fine (it's loopback) -- but nothing listens on this port,
# so the FAILURE happens one layer LATER, at the TCP handshake, not at DNS at all (co-07).
CLOSED_HOST = "127.0.0.1"
CLOSED_PORT = 50080  # => deliberately unused in this entire topic's port range


def classify_failure(host: str, port: int) -> str:  # => tries DNS FIRST, then TCP, in that order  # fmt: skip
    try:  # => wrapped so a DNS failure doesn't crash -- it's reported, not raised uncaught
        socket.gethostbyname(host)  # => co-03: DNS resolution -- the FIRST layer that can fail  # fmt: skip
    except socket.gaierror as err:  # => "gai" = getaddrinfo -- the resolver itself failed  # fmt: skip
        return f"failed at DNS layer: {err}"

    try:  # => reached only if DNS succeeded -- this tries the NEXT layer down
        with socket.create_connection((host, port), timeout=5):  # => co-07: the SECOND layer  # fmt: skip
            return "connected successfully"
    except ConnectionRefusedError as err:  # => DNS succeeded, but nobody answered on this port  # fmt: skip
        return f"failed at TCP layer: {err}"


dns_failure = classify_failure(BAD_HOST, 80)  # => guaranteed to fail at DNS, never reaches TCP  # fmt: skip
tcp_failure = classify_failure(CLOSED_HOST, CLOSED_PORT)  # => DNS succeeds, TCP is what fails  # fmt: skip

print(f"{BAD_HOST}:80 -> {dns_failure}")
print(f"{CLOSED_HOST}:{CLOSED_PORT} -> {tcp_failure}")

assert dns_failure.startswith("failed at DNS layer")  # => the bad host never even got an IP  # fmt: skip
assert tcp_failure.startswith("failed at TCP layer")  # => this host resolved fine; TCP refused  # fmt: skip
# co-01: this is `layering-and-leaks` made concrete -- the SAME exception-handling shape
# (try resolve, try connect) surfaces two COMPLETELY different failures at two DIFFERENT
# layers, and telling them apart is exactly what makes a real outage debuggable.
print("ex-80 OK")  # => confirms both distinct failure layers were correctly classified
