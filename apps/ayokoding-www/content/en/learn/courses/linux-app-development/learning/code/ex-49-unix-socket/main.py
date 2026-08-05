"""Exchange a real request and reply over a Unix-domain socket."""

import socket
import tempfile
import threading
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "notes.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen(1)

        def reply():
            connection, _ = server.accept()
            with connection:
                assert connection.recv(16) == b"STATUS"
                connection.sendall(b"OK")

        worker = threading.Thread(target=reply)
        worker.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(path))
            client.sendall(b"STATUS")
            print(client.recv(16).decode())
        worker.join()
