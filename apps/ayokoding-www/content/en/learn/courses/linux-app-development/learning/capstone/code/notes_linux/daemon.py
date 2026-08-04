import argparse
import logging
import signal
import socket
from pathlib import Path

from .core import socket_path, status_reply


def serve(path: Path) -> int:
    running = True

    def request_stop(_number, _frame):
        nonlocal running
        running = False

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    path.unlink(missing_ok=True)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen()
        server.settimeout(0.1)
        logging.info("listening on %s", path)
        while running:
            try:
                connection, _ = server.accept()
            except socket.timeout:
                continue
            with connection:
                connection.sendall(status_reply(connection.recv(1024)))
    path.unlink(missing_ok=True)
    logging.info("stopped cleanly")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="notes-linux-daemon")
    parser.add_argument("--socket", default="/tmp/notes-linux.sock")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    return serve(socket_path(args.socket))


if __name__ == "__main__":
    raise SystemExit(main())
