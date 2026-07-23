"""Example 29: TCP Echo Server."""

import socket  # => stdlib Berkeley sockets API (co-10)

HOST = "127.0.0.1"  # => loopback only -- this server never leaves the local machine
PORT = 50029  # => an ephemeral, unregistered port well above the well-known range (co-05)  # fmt: skip


def run_server() -> None:  # => binds, listens, accepts ONE client, echoes, then exits
    # socket.AF_INET selects IPv4; SOCK_STREAM selects TCP (co-07 reliable byte stream).
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        # => "with" scopes the socket's lifetime to this block -- it closes automatically
        # => even if an exception fires below, so a crashed server never leaks the fd
        # SO_REUSEADDR lets an immediate restart reuse a port stuck in TIME_WAIT --
        # Example 38 examines this option in depth; every server script in this topic
        # sets it so repeated runs never collide on a leftover TIME_WAIT socket.
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # => must be set BEFORE bind() -- setting it after bind() has no effect at all
        server_sock.bind((HOST, PORT))  # => claims (HOST, PORT) -- fails if already in use  # fmt: skip
        server_sock.listen(1)  # => marks the socket passive: ready to queue incoming connections  # fmt: skip
        print(f"listening on {HOST}:{PORT}")  # => a signal the client script waits for
        conn, addr = server_sock.accept()  # => BLOCKS until a client connects (co-07 handshake)  # fmt: skip
        # => conn is a NEW socket dedicated to this one client; addr is the client's (ip, port)
        with conn:
            # => conn's own "with" is a SEPARATE lifetime from server_sock's -- closing
            # => this one client's socket never touches the still-listening server_sock
            print(f"accepted connection from {addr}")
            # => proves accept() genuinely returned, not merely that a SYN packet arrived
            data = conn.recv(1024)  # => reads up to 1024 bytes sent by the client, blocking  # fmt: skip
            print(f"received: {data!r}")
            # => shows the raw bytes BEFORE echoing, so the transcript reads as a clear pair
            conn.sendall(data)  # => echoes the EXACT bytes back -- sendall loops until all sent  # fmt: skip


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    run_server()
    # => the guard above is WHY this call never fires if another script imports this module
