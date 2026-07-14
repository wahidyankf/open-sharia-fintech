"""Example 6: Raw 404."""

from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class NotFoundHandler(BaseHTTPRequestHandler):  # => one instance created per request
    """Handler that returns 404 for every path except the one known route."""

    # => do_GET is the ONLY method defined -- BaseHTTPRequestHandler routes
    # => every incoming GET request to a method with exactly this name (co-06)
    def do_GET(self) -> None:  # => called automatically for every GET request
        """Only "/known" succeeds; anything else is an unknown resource."""
        if self.path == "/known":  # => the ONE path this server recognizes
            self.send_response(200)  # => a real resource -- 200 OK
            self.end_headers()  # => no extra headers needed for this demo
            self.wfile.write(b"found it")  # => confirms the known route ran
        else:  # => every path that is not exactly "/known" falls through here
            # => everything else (typos, unrelated paths, "/") lands here --
            # => RFC 9110 SS15.5.5: 404 means "no representation exists" (co-03)
            self.send_response(404)  # => no matching route -- 404 Not Found
            self.end_headers()  # => no extra headers needed for this demo either
            self.wfile.write(b"not found")  # => body explains the failure


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with NotFoundHandler as its
    # => per-connection request factory -- one instance created per request
    return HTTPServer(("127.0.0.1", port), NotFoundHandler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
