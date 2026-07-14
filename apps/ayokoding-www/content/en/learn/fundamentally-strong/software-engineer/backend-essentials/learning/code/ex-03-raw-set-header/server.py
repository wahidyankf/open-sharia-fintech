"""Example 3: Raw Set Header."""

from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class HeaderHandler(BaseHTTPRequestHandler):  # => one instance created per request
    """Handler that sets one explicit response header before ending headers."""

    # => do_GET is the ONLY method defined -- BaseHTTPRequestHandler routes
    # => every incoming GET request to a method with exactly this name (co-06)
    def do_GET(self) -> None:  # => called automatically for every GET request
        """send_header() queues a header; end_headers() flushes them all."""
        self.send_response(200)  # => status line first, per HTTP's wire order
        self.send_header("Content-Type", "text/plain")  # => queues ONE header
        # => a name/value pair; call send_header() again per additional header
        self.end_headers()  # => writes every queued header, then a blank line
        # => nothing is sent to the socket until THIS call flushes the queue
        self.wfile.write(b"plain text body")  # => the body, matching that
        # => Content-Type: a client can now safely treat this as plain text


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with HeaderHandler as its
    # => per-connection request factory -- one HeaderHandler instance per request
    return HTTPServer(("127.0.0.1", port), HeaderHandler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
