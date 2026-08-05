import argparse
import socket
import sys
from pathlib import Path

from .core import socket_path


def request_status(path: Path) -> str:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(str(path))
        client.sendall(b"STATUS")
        return client.recv(1024).decode("utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="notes-linux")
    parser.add_argument("command", choices=["status"])
    parser.add_argument("--socket", default="/tmp/notes-linux.sock")
    args = parser.parse_args(argv)
    try:
        print(request_status(socket_path(args.socket)))
        return 0
    except OSError as error:
        print(f"notes-linux: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
