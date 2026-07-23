"""Example 8: Handle GET Only."""

from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class GetOnlyHandler(BaseHTTPRequestHandler):  # => one instance created per request
    """This handler implements only do_GET -- no do_POST, do_PUT, etc. at all."""

    def do_GET(self) -> None:  # => called automatically for every GET request
        """The only method this handler understands."""
        self.send_response(200)  # => a GET request finds a matching do_GET
        self.end_headers()  # => no extra headers needed for this demo
        self.wfile.write(b"get succeeded")  # => confirms this branch ran

    # => deliberately no do_POST/do_PUT/do_DELETE defined anywhere below --
    # => BaseHTTPRequestHandler's default behavior for a MISSING do_* method
    # => is to reply 501 Not Implemented (not 405 -- see Example 9 for that)


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with GetOnlyHandler as its
    # => per-connection request factory -- one instance created per request
    return HTTPServer(("127.0.0.1", port), GetOnlyHandler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
