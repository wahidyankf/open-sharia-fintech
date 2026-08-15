from __future__ import annotations

from hashlib import sha1
from pathlib import Path
import tempfile
import zlib


def encode(kind: str, payload: bytes) -> bytes:
    return f"{kind} {len(payload)}".encode() + b"\\0" + payload


def write_blob(root: Path, payload: bytes) -> str:
    raw = encode("blob", payload)
    identifier = sha1(raw).hexdigest()
    target = root / "objects" / identifier[:2] / identifier[2:]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(zlib.compress(raw))
    return identifier


def read_blob(root: Path, identifier: str) -> bytes:
    raw = zlib.decompress(
        (root / "objects" / identifier[:2] / identifier[2:]).read_bytes()
    )
    header, payload = raw.split(b"\\0", 1)
    if not header.startswith(b"blob "):
        raise ValueError("not a blob")
    return payload


def move_branch(root: Path, name: str, identifier: str) -> None:
    ref = root / "refs" / "heads" / name
    ref.parent.mkdir(parents=True, exist_ok=True)
    ref.write_text(identifier + "\n", encoding="utf-8")


def demo() -> tuple[str, bytes]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        identifier = write_blob(root, b"hello")
        move_branch(root, "main", identifier)
        return identifier, read_blob(root, identifier)
