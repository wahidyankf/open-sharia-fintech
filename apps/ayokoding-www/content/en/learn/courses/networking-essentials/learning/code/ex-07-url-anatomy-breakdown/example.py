# ex-07: urlsplit parses a URL into its five named components (co-02)
from urllib.parse import urlsplit

parts = urlsplit("https://host:443/path?q=1")  # => parses the URL structurally, not by eye  # fmt: skip
print("scheme:", parts.scheme)  # => the protocol: what speaks over the connection
print("host:", parts.hostname)  # => WHO to connect to -- resolved via DNS (co-03)
print("port:", parts.port)  # => WHICH service on that host -- 443 here (co-05)
print("path:", parts.path)  # => WHICH resource on that server
print("query:", parts.query)  # => extra parameters, after the "?"
