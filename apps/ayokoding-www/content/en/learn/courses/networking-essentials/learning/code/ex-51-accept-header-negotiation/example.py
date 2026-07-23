"""Example 51: Accept Header Negotiation -- Ask for JSON, Get JSON."""

import socket  # => stdlib sockets -- no HTTP library involved on either side of this exchange
import threading  # => only the ready-signal + background thread, not real concurrency

HOST = "127.0.0.1"  # => loopback -- keeps this negotiation demo local and deterministic
PORT = 50051  # => co-05: a fresh ephemeral port, unique to this example


def server(ready: threading.Event) -> None:  # => co-22: a server that reads the Accept header  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        # => IPv4 + TCP, scoped to this "with" block so the fd always closes on exit
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => set BEFORE bind() -- lets an immediate re-run reuse a TIME_WAIT'd port
        sock.bind((HOST, PORT))
        # => claims (HOST, PORT) for this process -- must happen before listen()
        sock.listen(1)
        # => flips the socket passive, ready to queue one pending connection
        ready.set()
        # => unblocks the main thread's wait() below -- no guessed sleep() needed
        conn, _ = sock.accept()
        # => BLOCKS until the client's connect() completes the TCP handshake
        with conn:  # => this one connection's socket -- closes automatically on block exit  # fmt: skip
            request = conn.recv(4096).decode()  # => reads the raw request bytes, decoded to text  # fmt: skip
            wants_json = "Accept: application/json" in request  # => co-16: read ONE header's value  # fmt: skip
            if wants_json:  # => co-22: the client's Accept header decides the representation  # fmt: skip
                body = b'{"greeting": "hello"}'  # => the JSON representation of the SAME greeting
                content_type = b"application/json"  # => the Content-Type that MATCHES the body  # fmt: skip
            else:
                # => the safe fallback when Accept doesn't ask for JSON explicitly
                body = b"greeting: hello"  # => the plain-text representation of the SAME greeting
                content_type = b"text/plain"  # => the Content-Type that MATCHES this body instead  # fmt: skip
            response = (  # => built by hand, byte by byte -- no HTTP library involved
                b"HTTP/1.1 200 OK\r\n"  # => co-13: the status line -- version, code, reason phrase
                # => the negotiated type, not hardcoded
                b"Content-Type: " + content_type + b"\r\n"
                # => the actual body's size
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"Connection: close\r\n"  # => tells the client to expect the connection to close
                # => the mandatory blank-line separator, then the chosen body
                b"\r\n" + body
            )
            conn.sendall(response)  # => the chosen representation, sent back over this connection  # fmt: skip


ready_event = threading.Event()  # => the same ready-signal pattern used since Example 34  # fmt: skip
thread = threading.Thread(target=server, args=(ready_event,), daemon=True)
# => daemon=True: this thread never blocks process exit if something above hangs
thread.start()
# => runs the server concurrently with the request-sending client code that follows
ready_event.wait(timeout=5)
# => blocks here until bind()+listen() genuinely completed, avoiding a race with connect()

request = (  # => plain string concatenation -- no HTTP library builds this for us either
    "GET / HTTP/1.1\r\n"  # => the request line: METHOD, PATH, VERSION
    "Host: 127.0.0.1\r\n"  # => co-16: HTTP/1.1 REQUIRES a Host header even on loopback
    "Accept: application/json\r\n"  # => co-22: explicitly asking for JSON, not plain text
    "Connection: close\r\n"  # => tells the server to close after replying, simplifying this demo
    "\r\n"  # => the blank line that ends the headers -- REQUIRED even with no body
)
with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => co-07: the TCP handshake  # fmt: skip
    sock.sendall(request.encode())  # => co-12: the raw hand-built request, sent as bytes  # fmt: skip
    response = b""  # => accumulates the full response -- its final size isn't known upfront  # fmt: skip
    while True:  # => co-11: loop until the server closes (Connection: close makes this safe)  # fmt: skip
        chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
        if not chunk:  # => an empty recv() means the server closed its side
            break
        response += chunk  # => appends this chunk -- the loop above may run several times  # fmt: skip

thread.join(timeout=5)
# => waits for the server thread to finish handling this one request before exiting

head, _, body = response.partition(b"\r\n\r\n")  # => co-13: split at the one fixed boundary  # fmt: skip
print(f"headers:\n{head.decode()}")  # => expect Content-Type: application/json in this output  # fmt: skip
print(f"body: {body!r}")  # => expect the JSON body, since the request's Accept asked for JSON  # fmt: skip

assert b"application/json" in head  # => confirms the server chose JSON based on Accept
assert body == b'{"greeting": "hello"}'  # => confirms the BODY is actually JSON, not plain text  # fmt: skip
# both assertions together confirm negotiation is genuine: the Content-Type header and the
# actual body bytes agree with each other, and both were driven by what the client asked for.
print("ex-51 OK")  # => confirms the Accept -> Content-Type negotiation worked end to end  # fmt: skip
