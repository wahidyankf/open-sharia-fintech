"""Example 41: Raw HTTP with nc -- Local HTTP Responder."""

import socket  # => stdlib sockets -- this server writes its own HTTP text by hand, no library

HOST = "127.0.0.1"  # => loopback -- nc connects locally in this sandboxed environment
PORT = 50041  # => co-05: nc will target this exact port on the command line


def run_server() -> None:  # => a minimal, hand-rolled HTTP/1.1 responder (co-12, co-13)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:  # => same triple as Ex 29+  # fmt: skip
        # => IPv4 + TCP, scoped to this "with" block so the fd always closes on exit
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => set BEFORE bind() -- lets an immediate re-run reuse a TIME_WAIT'd port
        sock.bind((HOST, PORT))
        # => claims (HOST, PORT) for this process -- must happen before listen()
        sock.listen(1)
        # => flips the socket passive, ready to queue nc's one incoming connection
        print(f"listening on {HOST}:{PORT}", flush=True)  # => the signal nc's caller waits for  # fmt: skip
        conn, _ = sock.accept()  # => accepts nc's raw TCP connection, no TLS involved
        with conn:  # => nc's connected socket -- closes automatically when this block exits  # fmt: skip
            request = conn.recv(4096)  # => reads whatever raw bytes nc piped in verbatim  # fmt: skip
            print(f"server saw raw request bytes:\n{request.decode(errors='replace')}")  # => co-12  # fmt: skip
            body = b"hello from a hand-rolled HTTP responder\n"  # => co-13: the response body
            # co-12/co-13: a real status line, real headers, a blank line, then the body --
            # this is EXACTLY the message shape ex-05/ex-06 identified inside curl -v earlier.
            response = (  # => built by hand, byte by byte -- no HTTP library involved
                b"HTTP/1.1 200 OK\r\n"  # => co-13: the status line -- version, code, reason phrase
                b"Content-Type: text/plain\r\n"
                # => body size, not a guess -- computed, never hardcoded
                b"Content-Length: " + str(len(body)).encode() + b"\r\n"
                b"Connection: close\r\n"
                # => the mandatory blank-line separator, then the raw body bytes
                b"\r\n" + body
            )
            conn.sendall(response)  # => nc prints these exact raw bytes to its own stdout  # fmt: skip


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    run_server()  # => the guard above is WHY this only fires when this file is run as a script
