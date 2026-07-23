"""Example 5: Raw JSON Response."""

import json  # => standard library's JSON encoder/decoder, no dependency needed
from http.server import BaseHTTPRequestHandler, HTTPServer  # => imports the base class + server


class JsonHandler(BaseHTTPRequestHandler):  # => one instance created per request
    """Handler that hand-serializes a dict to JSON bytes."""

    # => do_GET is the ONLY method defined -- BaseHTTPRequestHandler routes
    # => every incoming GET request to a method with exactly this name (co-06)
    def do_GET(self) -> None:  # => called automatically for every GET request
        """json.dumps() turns a typed dict into a JSON string, then bytes."""
        payload: dict[str, str | int] = {"msg": "hello", "code": 1}
        # => payload is an ordinary typed Python dict -- json.dumps() below
        # => is the ONLY step turning it into JSON; nothing does this for you
        body: bytes = json.dumps(payload).encode("utf-8")  # str -> bytes
        # => .encode("utf-8") is required: wfile.write() only accepts bytes
        self.send_response(200)  # => status line, before any header is queued
        self.send_header("Content-Type", "application/json")  # => tells the
        # => client (and co-21's content-negotiation) this body is JSON, not text
        self.end_headers()  # => flushes the queued Content-Type header
        self.wfile.write(body)  # => writes the encoded JSON bytes as the body


def run(port: int) -> HTTPServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    # => HTTPServer pairs a listening socket with JsonHandler as its
    # => per-connection request factory -- one JsonHandler instance per request
    return HTTPServer(("127.0.0.1", port), JsonHandler)
    # => binds to localhost only; caller decides when to start serving


if __name__ == "__main__":  # => only runs when executed directly, not on import
    # => run() only BUILDS the server; serve_forever() is the call that
    # => actually starts accepting connections and blocks this process
    run(8000).serve_forever()  # => blocks, handling one request at a time
