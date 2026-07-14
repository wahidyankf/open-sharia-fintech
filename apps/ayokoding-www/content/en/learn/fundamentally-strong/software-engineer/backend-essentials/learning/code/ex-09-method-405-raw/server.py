"""Example 9: Method 405 Raw."""

from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class GetOnlyWith405Handler(BaseHTTPRequestHandler):  # => one instance per request
    """A GET-only resource that hand-writes a proper 405 for other methods."""

    def do_GET(self) -> None:  # => called automatically for every GET request
        """The one method this route actually supports."""
        self.send_response(200)  # => the only method this route accepts
        self.end_headers()  # => no extra headers needed for this demo
        self.wfile.write(b"get succeeded")  # => confirms GET reached here

    def do_POST(self) -> None:  # => called automatically for every POST request
        """RFC 9110 SS15.5.6: a 405 response MUST include an Allow header."""
        # => do_POST is defined ON PURPOSE here (unlike Example 8) so this
        # => handler can reply with a PRECISE 405, not the stdlib's generic 501
        self.send_response(405)  # => Method Not Allowed (co-02, co-03)
        self.send_header("Allow", "GET")  # => tells the client which methods
        # => ARE ok -- this header is mandatory per RFC 9110, not optional
        self.end_headers()  # => flushes the queued Allow header
        self.wfile.write(b"method not allowed")  # => explains the rejection


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with GetOnlyWith405Handler as its
    # => per-connection request factory -- one instance created per request
    return HTTPServer(("127.0.0.1", port), GetOnlyWith405Handler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
