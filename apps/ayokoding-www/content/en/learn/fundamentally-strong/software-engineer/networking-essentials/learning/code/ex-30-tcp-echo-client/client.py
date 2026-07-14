"""Example 30: TCP Echo Client."""

import socket  # => same stdlib sockets API the server uses (co-10)

HOST = "127.0.0.1"  # => must match the server's bound address exactly
PORT = 50029  # => must match the server's bound port exactly (co-05)


def run_client(message: bytes) -> bytes:  # => connects, sends one message, returns the echo  # fmt: skip
    # socket.create_connection is a convenience wrapper: resolve + connect in one call (co-01).
    with socket.create_connection((HOST, PORT)) as sock:  # => performs the TCP handshake  # fmt: skip
        sock.sendall(message)  # => writes every byte of message onto the connection
        return sock.recv(1024)  # => reads the server's echoed reply, up to 1024 bytes


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    # run_client is a plain function returning bytes -- kept separate from the printing/
    # asserting below so it could be imported and reused elsewhere without any side effects
    reply = run_client(b"hello from ex-30 client\n")  # => Example 29's server must already be up  # fmt: skip
    print(f"client received: {reply!r}")  # => confirms the echoed bytes match what was sent  # fmt: skip
    assert reply == b"hello from ex-30 client\n"  # => proves the round trip preserved every byte  # fmt: skip
    print("ex-30 OK")  # => a final marker confirming every assertion above passed, not just ran  # fmt: skip
