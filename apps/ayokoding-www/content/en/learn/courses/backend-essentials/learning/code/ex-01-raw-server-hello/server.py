"""Example 1: Raw Server Hello."""

# => http.server is the standard library's minimal HTTP toolkit -- no
# => third-party package is installed for this example or the next 8 (co-06)
from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


# => subclassing BaseHTTPRequestHandler gets request PARSING for free (method,
# => path, headers); everything about the RESPONSE below is still hand-written
class HelloHandler(BaseHTTPRequestHandler):  # => one instance is created per request
    """A hand-written request handler -- no framework routing at all."""

    # => do_GET is a MAGIC method name: BaseHTTPRequestHandler dispatches every
    # => incoming GET request to a method named exactly "do_GET" (co-06)
    def do_GET(self) -> None:  # => called automatically for every GET request
        """Handle every GET request the same way: reply with 'hello'."""
        self.send_response(200)  # => writes the status line "HTTP/1.0 200 OK"
        # => must happen BEFORE any send_header() calls -- order matters (co-01)
        self.send_header("Content-Type", "text/plain")  # => queues one header
        # => queued, not written yet -- end_headers() flushes it (co-04)
        self.end_headers()  # => writes every queued header + a blank line
        # => that blank line marks the end of the header block (RFC 9110, co-01)
        self.wfile.write(b"hello")  # => writes the raw body bytes
        # => wfile is the socket's write-file object; bytes, not str (co-01)


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => 127.0.0.1 binds to localhost only -- unreachable from other machines
    server = HTTPServer(("127.0.0.1", port), HelloHandler)
    # => pairs a listening socket with HelloHandler as its request factory
    return server  # => caller decides exactly when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => serve_forever() blocks, handling one request at a time in this loop
    run(8000).serve_forever()  # => builds the server, then starts it serving
