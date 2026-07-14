"""Example 2: Raw Status Line."""

from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class StatusHandler(BaseHTTPRequestHandler):  # => one instance created per request
    """Handler that writes the status line and headers as two explicit calls."""

    # => do_GET is the ONLY method defined -- BaseHTTPRequestHandler routes
    # => every incoming GET request to a method with exactly this name (co-06)
    def do_GET(self) -> None:  # => called automatically for every GET request
        """send_response() writes the status line; end_headers() ends the block."""
        self.send_response(200)  # => IMMEDIATELY writes "HTTP/1.0 200 OK\r\n"
        # => the first argument is the numeric status; the reason phrase
        # => ("OK") is looked up automatically from the status code (co-03)
        self.end_headers()  # => no extra headers queued -- just the blank line
        # => that terminates the header block, per RFC 9110 SS15 (co-01)
        self.wfile.write(b"status ok")  # => the response body, as raw bytes
        # => arrives on the wire AFTER the status line and headers above


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with StatusHandler as its
    # => per-connection request factory -- one StatusHandler instance per request
    return HTTPServer(("127.0.0.1", port), StatusHandler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
