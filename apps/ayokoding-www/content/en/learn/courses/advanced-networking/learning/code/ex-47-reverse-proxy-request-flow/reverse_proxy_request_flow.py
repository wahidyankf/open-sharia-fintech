# learning/code/ex-47-reverse-proxy-request-flow/reverse_proxy_request_flow.py
"""Example 47: A Local Reverse Proxy -- Forwarding a Client Request to a Backend."""  # => co-20: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import http.client  # => co-20: the PROXY's own outbound client -- how it forwards to the backend, stdlib-only
import threading  # => co-20: runs the backend and the proxy concurrently, both listening on their own localhost ports
import time  # => co-20: a brief pause so both servers are genuinely listening before the client below connects
from http.server import BaseHTTPRequestHandler, HTTPServer  # => co-20: stdlib-only HTTP server, used for BOTH the backend and the proxy

HOST = "127.0.0.1"  # => co-20: loopback -- this demo needs no real network, only two real local HTTP servers


class BackendHandler(BaseHTTPRequestHandler):  # => co-20: the ORIGIN server -- what a reverse proxy sits in front of
    def log_message(self, format: str, *args: object) -> None:  # => co-20: silences BaseHTTPRequestHandler's default per-request stderr logging
        """Suppress the base class's default request logging -- keeps this demo's own prints the only output."""  # => co-20: documents log_message's contract -- no runtime output, just sets its __doc__
        pass  # => co-20: intentionally empty -- overriding to do nothing is the standard stdlib way to silence it

    def do_GET(self) -> None:  # => co-20: the backend's own response -- the client below never talks to this directly
        body = b"hello from backend"  # => co-20: a fixed, recognizable payload -- proves the FINAL response really did originate here
        self.send_response(200)  # => co-20: an ordinary 200 -- the backend has no idea a proxy is in front of it
        self.send_header("Content-Length", str(len(body)))  # => co-20: required so the client (the proxy, in this case) knows exactly where the body ends
        self.send_header("X-Served-By", "backend")  # => co-20: a marker header this demo's own asserts check for, proving the ORIGIN handled the request
        self.end_headers()  # => co-20: ends the header block -- everything written after this is the response body
        self.wfile.write(body)  # => co-20: writes the fixed payload onto the response socket


def make_proxy_handler(backend_port: int) -> type[BaseHTTPRequestHandler]:  # => co-20: a factory -- bakes the backend's port into a fresh handler CLASS, since http.server takes a class, not an instance
    """Build a reverse-proxy handler class that forwards every GET to the backend on `backend_port`."""  # => co-20: documents make_proxy_handler's contract -- no runtime output, just sets its __doc__

    class ProxyHandler(BaseHTTPRequestHandler):  # => co-20: THE reverse proxy -- co-20's "sits in front of an origin server" role, in code
        def log_message(self, format: str, *args: object) -> None:  # => co-20: silences BaseHTTPRequestHandler's default per-request stderr logging
            """Suppress the base class's default request logging -- keeps this demo's own prints the only output."""  # => co-20: documents log_message's contract -- no runtime output, just sets its __doc__
            pass  # => co-20: intentionally empty -- overriding to do nothing is the standard stdlib way to silence it

        def do_GET(self) -> None:  # => co-20: THE forwarding step -- everything the client sees comes from this method, not from the backend directly
            upstream = http.client.HTTPConnection(HOST, backend_port)  # => co-20: the proxy opens its OWN, separate connection to the backend -- the client never sees this hop
            upstream.request("GET", self.path)  # => co-20: forwards the SAME path the client requested -- a real proxy would also forward headers/method/body
            backend_response = upstream.getresponse()  # => co-20: reads the backend's full response, on the proxy's side of the wire
            backend_body = backend_response.read()  # => co-20: the exact bytes the backend sent, read here before relaying them onward
            self.send_response(backend_response.status)  # => co-20: relays the backend's OWN status code -- the proxy does not invent one
            self.send_header("Content-Length", str(len(backend_body)))  # => co-20: required so the ORIGINAL client knows where the relayed body ends
            self.send_header("X-Served-By", backend_response.getheader("X-Served-By", ""))  # => co-20: relays the BACKEND's own marker header through unchanged -- proves headers, not just the body, survive the hop
            self.send_header("X-Proxied-By", "reverse-proxy")  # => co-20: a marker header this demo's own asserts check for, proving the PROXY (not the backend) answered the client
            self.end_headers()  # => co-20: ends the header block -- everything written after this is the relayed response body
            self.wfile.write(backend_body)  # => co-20: relays the backend's exact bytes back to the ORIGINAL client -- the client never touched the backend
            upstream.close()  # => co-20: releases the proxy-to-backend connection's resources

    return ProxyHandler  # => co-20: returns this computed value to the caller


if __name__ == "__main__":  # => co-20: entry point -- this block runs only when the file executes directly, not on import
    backend_server = HTTPServer((HOST, 0), BackendHandler)  # => co-20: port 0 -- let the OS pick a free ephemeral port for the ORIGIN
    backend_port = backend_server.server_port  # => co-20: the OS-assigned backend port -- the client below must NEVER see or use this directly
    threading.Thread(target=backend_server.serve_forever, daemon=True).start()  # => co-20: runs the backend's request loop concurrently

    proxy_server = HTTPServer((HOST, 0), make_proxy_handler(backend_port))  # => co-20: port 0 -- a SEPARATE free ephemeral port for the PROXY
    proxy_port = proxy_server.server_port  # => co-20: the OS-assigned proxy port -- this IS the address the client below connects to
    threading.Thread(target=proxy_server.serve_forever, daemon=True).start()  # => co-20: runs the proxy's request loop concurrently
    time.sleep(0.1)  # => co-20: a brief pause so both servers are genuinely listening before the client below connects

    client = http.client.HTTPConnection(HOST, proxy_port)  # => co-20: the CLIENT -- connects ONLY to the proxy's address, exactly as co-20 describes
    client.request("GET", "/")  # => co-20: an ordinary GET -- the client has no idea a backend even exists behind this address
    response = client.getresponse()  # => co-20: reads the response the PROXY relayed back
    response_headers = dict(response.getheaders())  # => co-20: captures every header for inspection below
    response_body = response.read()  # => co-20: the final bytes the client actually received
    client.close()  # => co-20: releases the client-to-proxy connection's resources

    print(f"client connected to proxy port {proxy_port} only -- backend port {backend_port} was never dialed directly")  # => co-20: the headline claim, stated in terms of the ACTUAL ports used
    print(f"status: {response.status}")  # => co-20: the relayed status code, as observed by the client
    print(f"X-Proxied-By: {response_headers.get('X-Proxied-By')}")  # => co-20: confirms the PROXY's own marker header reached the client
    print(f"X-Served-By: {response_headers.get('X-Served-By')}")  # => co-20: confirms the BACKEND's marker header ALSO reached the client, relayed through
    print(f"body: {response_body!r}")  # => co-20: the backend's exact payload, unmodified by the proxy hop

    assert response.status == 200, "the relayed status must match the backend's own 200"  # => co-20
    assert response_headers.get("X-Proxied-By") == "reverse-proxy", "the client must see the PROXY's own marker header"  # => co-20
    assert response_headers.get("X-Served-By") == "backend", "the client must ALSO see the backend's marker header, relayed through"  # => co-20
    assert response_body == b"hello from backend", "the relayed body must exactly match the backend's own payload"  # => co-20
    print("The client observed the proxy's address, never the backend's, yet received the backend's exact response: True")  # => co-20: reached only if every assert above passed
    # => co-20: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
