"""Example 4: Raw Read Path."""

from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class PathHandler(BaseHTTPRequestHandler):  # => one instance created per request
    """Handler that branches on self.path -- no router, just an if/elif chain."""

    # => do_GET is the ONLY method defined -- BaseHTTPRequestHandler routes
    # => every incoming GET request to a method with exactly this name (co-06)
    def do_GET(self) -> None:  # => called automatically for every GET request
        """self.path holds the raw request path, e.g. "/a" or "/b?x=1"."""
        # => self.path is set by BaseHTTPRequestHandler BEFORE do_GET runs,
        # => parsed straight from the request line's second token (co-06)
        if self.path == "/a":  # => exact string match on the raw path
            body = b"route a"  # => this branch handles ONLY "/a" exactly
        elif self.path == "/b":  # => a second, independent exact match
            body = b"route b"  # => this branch handles ONLY "/b" exactly
        else:  # => catches every path that matched neither branch above
            body = b"unknown route"  # => anything else falls through here
            # => including "/", "/c", or "/a/nested" -- no partial matching
        self.send_response(200)  # => every branch above still returns 200
        self.end_headers()  # => no headers needed for this plain-text demo
        self.wfile.write(body)  # => writes whichever branch's body was chosen


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with PathHandler as its
    # => per-connection request factory -- one PathHandler instance per request
    return HTTPServer(("127.0.0.1", port), PathHandler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
