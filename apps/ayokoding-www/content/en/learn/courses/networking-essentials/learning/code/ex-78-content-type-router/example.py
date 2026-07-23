"""Example 78: A Server That Routes JSON or Plain Text by Accept Header."""  # => co-22 negotiation

import socket  # => stdlib sockets -- both rounds below build on this one module
import threading  # => a fresh server thread PER round, not one long-lived server

HOST = "127.0.0.1"  # => loopback -- keeps this two-round negotiation demo local and deterministic
PORT = 50078  # => co-05: reused across BOTH rounds, thanks to SO_REUSEADDR below


def build_response(accept_header: str) -> bytes:  # => co-22: content negotiation, both directions  # fmt: skip
    if "application/json" in accept_header:  # => co-22: the client explicitly asked for JSON  # fmt: skip
        body = b'{"status": "ok"}'  # => the JSON representation of the SAME status
        content_type = b"application/json"  # => the Content-Type that MATCHES the body  # fmt: skip
    else:  # => co-22: no JSON requested -- fall back to plain text, the safe default
        body = b"status: ok"  # => the plain-text representation of the SAME status
        content_type = b"text/plain"  # => the Content-Type that MATCHES this body instead  # fmt: skip
    return (  # => built by hand, byte by byte -- no HTTP library involved
        b"HTTP/1.1 200 OK\r\n"  # => co-13: the status line -- version, code, reason phrase
        # => the negotiated type, not hardcoded
        b"Content-Type: " + content_type + b"\r\n"
        # => the actual body's size
        b"Content-Length: " + str(len(body)).encode() + b"\r\n"
        b"Connection: close\r\n"  # => tells the client to expect the connection to close
        # => the mandatory blank-line separator, then the chosen body
        b"\r\n" + body
    )


def handle_one(port: int, ready: threading.Event) -> None:  # => a fresh single-shot server  # fmt: skip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # => lets round 2 reuse PORT  # fmt: skip
        sock.bind((HOST, port))  # => claims (HOST, port) for THIS round only
        sock.listen(1)  # => flips the socket passive, ready to queue one pending connection  # fmt: skip
        ready.set()  # => unblocks run_round()'s wait() below -- no guessed sleep() needed
        conn, _ = sock.accept()  # => BLOCKS until this round's client completes the handshake  # fmt: skip
        with conn:  # => this round's connection -- closes automatically on block exit
            request = conn.recv(4096).decode()  # => reads the raw request bytes, decoded to text  # fmt: skip
            accept_line = next(  # => finds the ONE header line this server actually cares about
                # => matches the Accept header, if the client sent one
                (line for line in request.split("\r\n") if line.startswith("Accept:")),
                "",
            )  # => "" if no Accept header was sent at all -- falls to the plain-text default
            conn.sendall(build_response(accept_line))  # => the negotiated reply, sent back  # fmt: skip


def request_with_accept(accept_value: str) -> bytes:  # => sends one GET with a chosen Accept value  # fmt: skip
    with socket.create_connection((HOST, PORT), timeout=5) as sock:  # => co-07: the TCP handshake  # fmt: skip
        request = f"GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nAccept: {accept_value}\r\nConnection: close\r\n\r\n"  # => co-22
        sock.sendall(request.encode())  # => co-12: the hand-built request, sent as raw bytes  # fmt: skip
        data = b""  # => accumulates the full response -- its final size isn't known in advance
        while True:  # => co-11: loop until the server closes (Connection: close makes this safe)  # fmt: skip
            chunk = sock.recv(4096)  # => reads whatever arrives next, up to 4096 bytes
            if not chunk:  # => an empty recv() means the server closed its side
                break  # => exits the loop -- the full response has now been fully read
            data += chunk  # => appends this chunk -- the loop above may run several times  # fmt: skip
    return data  # => the ONE value this function hands back to its caller


def run_round(accept_value: str) -> bytes:  # => co-01: one fresh server + one request, per round  # fmt: skip
    ready = threading.Event()  # => a NEW event per round -- this round's own ready-signal  # fmt: skip
    server_thread = threading.Thread(target=handle_one, args=(PORT, ready), daemon=True)  # => co-11  # fmt: skip
    server_thread.start()  # => runs THIS round's single-shot server concurrently
    ready.wait(timeout=5)  # => blocks until THIS round's bind()+listen() genuinely completed  # fmt: skip
    response = request_with_accept(accept_value)  # => sends the request, waits for the reply  # fmt: skip
    server_thread.join(timeout=5)  # => waits for THIS round's server to finish before returning  # fmt: skip
    return response  # => the ONE value this function hands back to its caller


# Round 1: client asks for JSON.
json_response = run_round("application/json")  # => a fresh server + one JSON-requesting client  # fmt: skip
json_head, _, json_body = json_response.partition(b"\r\n\r\n")  # => co-13: split at the boundary  # fmt: skip

# Round 2: client asks for plain text -- a FRESH server, same port, reused via SO_REUSEADDR.
text_response = run_round("text/plain")  # => a SECOND fresh server + one plain-text-requesting client  # fmt: skip
text_head, _, text_body = text_response.partition(b"\r\n\r\n")  # => co-13: split at the boundary  # fmt: skip

print(f"Accept: application/json -> {json_body!r}")  # => expect the JSON body from round 1  # fmt: skip
print(f"Accept: text/plain -> {text_body!r}")  # => expect the plain-text body from round 2  # fmt: skip

assert b"application/json" in json_head and json_body == b'{"status": "ok"}'  # => round 1 correct  # fmt: skip
assert b"text/plain" in text_head and text_body == b"status: ok"  # => round 2 correct
print("ex-78 OK")  # => confirms the SAME routing logic branched correctly both ways
