"""Example 60: Resolve a Hostname to an IP Address in Python."""

import socket  # => stdlib sockets -- both resolver functions below live in this one module

HOST = "example.com"  # => co-03: the same demo host every dig-based example resolved

# gethostbyname is the simple, IPv4-only resolver call -- co-03, co-10.
ipv4_address = socket.gethostbyname(
    HOST
)  # => a single blocking DNS lookup, returns one IPv4
print(
    f"gethostbyname: {ipv4_address}"
)  # => one address, no family/port metadata attached

# getaddrinfo is the modern, protocol-agnostic resolver -- returns EVERY matching address,
# IPv4 and IPv6 alike, plus the socket parameters needed to connect to each one (co-03).
results = socket.getaddrinfo(
    HOST, 80, proto=socket.IPPROTO_TCP
)  # => a richer, multi-result lookup
print(
    f"getaddrinfo returned {len(results)} result(s)"
)  # => count varies by host's IPv4/IPv6 records
# each getaddrinfo() result is a 5-tuple: family, socktype, proto, canonical name, sockaddr.
for family, _socktype, _proto, _canonname, sockaddr in results:
    family_name = (
        "IPv4" if family == socket.AF_INET else "IPv6"
    )  # => classifies THIS one result
    print(
        f"  {family_name}: {sockaddr[0]}"
    )  # => sockaddr[0] is the address; [1] is the port

assert ipv4_address.count(".") == 3  # => confirms a dotted-quad IPv4 address came back
assert len(results) >= 1  # => confirms getaddrinfo found at least one real address
print(
    "ex-60 OK"
)  # => confirms both resolver functions genuinely resolved the same host
