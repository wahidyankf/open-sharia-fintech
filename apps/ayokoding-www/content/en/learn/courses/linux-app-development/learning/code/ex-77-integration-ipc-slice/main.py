"""Exercise one end-to-end Unix-socket request/reply slice."""

import socket
import tempfile
import threading
from pathlib import Path


def reply(server):
    connection, _ = server.accept()
    with connection:
        connection.sendall(
            b"OK notes-daemon" if connection.recv(32) == b"STATUS" else b"ERROR"
        )


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "ipc.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen(1)
        worker = threading.Thread(target=reply, args=(server,))
        worker.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(path))
            client.sendall(b"STATUS")
            assert client.recv(32) == b"OK notes-daemon"
        worker.join()
print("integration passed")
