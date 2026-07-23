"""Example 7: wsgiref App."""

from collections.abc import Iterable  # => generic type for "iterable of X" annotations
from wsgiref.simple_server import WSGIServer, make_server  # => stdlib's reference WSGI server
from wsgiref.types import StartResponse, WSGIEnvironment  # => stdlib's PEP 3333 protocol types

# => StartResponse/WSGIEnvironment are the PEP 3333 stdlib protocol types --
# => this is the SAME callable signature every WSGI framework (Flask included)
# => implements underneath, which is why co-06 calls this "what a framework
# => automates" -- Flask's app object IS a function shaped exactly like this


def app(environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]:
    """A WSGI callable: takes environ + start_response, returns an iterable of bytes."""
    # => environ carries the parsed request (method, path, headers) as a dict;
    # => this example ignores it entirely and answers every request identically
    start_response("200 OK", [("Content-Type", "text/plain")])  # status + headers
    # => start_response is a CALLBACK the server passes in -- calling it is
    # => how a WSGI app "returns" its status line, unlike a normal return value
    return [b"wsgi hello"]  # => body, as an iterable of byte-strings
    # => WSGI requires an ITERABLE of bytes, not a single bytes object


def run(port: int) -> WSGIServer:  # => builds, but does not yet start, the server
    """Build and return a server bound to the given port (caller starts it)."""
    return make_server("127.0.0.1", port, app)
    # => wires `app` above into a real socket server -- binds localhost only


if __name__ == "__main__":  # => only runs when executed directly, not on import
    run(8000).serve_forever()  # => blocks, handling one request at a time
