"""Keep the CLI and daemon on one protocol core."""


def status_reply(command: bytes) -> bytes:
    return b"OK notes-daemon" if command == b"STATUS" else b"ERROR unknown command"


print(status_reply(b"STATUS").decode())
