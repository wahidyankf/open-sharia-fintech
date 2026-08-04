from pathlib import Path


def socket_path(value: str) -> Path:
    """Return the caller-selected Unix-socket location."""
    return Path(value)


def status_reply(command: bytes) -> bytes:
    """Keep the tiny protocol deterministic and testable."""
    return b"OK notes-daemon" if command == b"STATUS" else b"ERROR unknown command"
