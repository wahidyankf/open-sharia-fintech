"""Serve one IPC request from a Unix-socket daemon."""

import socket
import tempfile
import threading
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "daemon.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen(1)

        def serve_one():
            connection, _ = server.accept()
            with connection:
                command = connection.recv(32)
                connection.sendall(
                    b"OK notes-daemon" if command == b"STATUS" else b"ERROR"
                )

        worker = threading.Thread(target=serve_one)
        worker.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(path))
            client.sendall(b"STATUS")
            print(client.recv(32).decode())
        worker.join()
