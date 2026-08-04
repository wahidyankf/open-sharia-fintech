"""Exchange a real request and reply over localhost TCP."""

import socket
import threading

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    host, port = server.getsockname()

    def reply():
        connection, _ = server.accept()
        with connection:
            assert connection.recv(16) == b"PING"
            connection.sendall(b"PONG")

    worker = threading.Thread(target=reply)
    worker.start()
    with socket.create_connection((host, port)) as client:
        client.sendall(b"PING")
        print(client.recv(16).decode())
    worker.join()
