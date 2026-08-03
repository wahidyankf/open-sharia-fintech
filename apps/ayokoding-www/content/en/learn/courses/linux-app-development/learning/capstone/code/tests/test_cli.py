import socket
import tempfile
import threading
from pathlib import Path

from notes_linux import cli


def test_status_prints_reply_from_live_server(capsys):
    # AF_UNIX paths have a platform limit, so keep the unique test socket under /tmp.
    with tempfile.TemporaryDirectory(prefix="nl-", dir="/tmp") as directory:
        path = Path(directory) / "s"
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
            server.bind(str(path))
            server.listen(1)

            def serve_status():
                connection, _ = server.accept()
                with connection:
                    assert connection.recv(1024) == b"STATUS"
                    connection.sendall(b"OK notes-daemon")

            worker = threading.Thread(target=serve_status)
            worker.start()
            assert cli.main(["status", "--socket", str(path)]) == 0
            worker.join(timeout=1)
            assert not worker.is_alive()
    captured = capsys.readouterr()
    assert captured.out == "OK notes-daemon\n"
    assert captured.err == ""


def test_unavailable_socket_is_stderr(tmp_path, capsys):
    assert cli.main(["status", "--socket", str(tmp_path / "none.sock")]) == 1
    assert "notes-linux:" in capsys.readouterr().err
