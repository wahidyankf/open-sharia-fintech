# ex-07: urlsplit parses a URL into its five named components (co-02)
from urllib.parse import urlsplit

parts = urlsplit("https://host:443/path?q=1")
print("scheme:", parts.scheme)
print("host:", parts.hostname)
print("port:", parts.port)
print("path:", parts.path)
print("query:", parts.query)
