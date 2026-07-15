"""A minimal, real Debug Adapter Protocol (DAP) client -- just enough to attach to a debugpy
listener, set one breakpoint, let it hit, and read one local variable. debugpy implements the
DAP over a plain TCP socket carrying Content-Length-framed JSON messages (the same framing VS
Code's own DAP client uses) -- this talks that real protocol directly, no debugpy-bundled client
library needed.
"""

from __future__ import annotations

import json
import socket
import threading
import time


class DapClient:
    def __init__(self, host: str, port: int) -> None:
        self.sock = socket.create_connection((host, port), timeout=10)
        self.seq = 0
        self.buffer = b""
        self.events: list[dict] = []
        self.lock = threading.Lock()
        self.reader = threading.Thread(target=self._read_loop, daemon=True)
        self.reader.start()

    def _read_loop(self) -> None:
        while True:
            try:
                data = self.sock.recv(4096)
            except OSError:
                return
            if not data:
                return
            with self.lock:
                self.buffer += data

    def _pop_message(self, timeout: float = 5.0) -> dict | None:
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self.lock:
                if b"\r\n\r\n" in self.buffer:
                    header, rest = self.buffer.split(b"\r\n\r\n", 1)
                    length = int(header.split(b":")[1].strip())
                    if len(rest) >= length:
                        body, remaining = rest[:length], rest[length:]
                        self.buffer = remaining
                        return json.loads(body)
            time.sleep(0.02)
        return None

    def send(self, msg_type: str, command: str, arguments: dict | None = None) -> int:
        self.seq += 1
        msg = {"seq": self.seq, "type": msg_type, "command": command}
        if arguments is not None:
            msg["arguments"] = arguments
        body = json.dumps(msg).encode()
        header = f"Content-Length: {len(body)}\r\n\r\n".encode()
        self.sock.sendall(header + body)
        return self.seq

    def wait_for(self, predicate, timeout: float = 10.0) -> dict:
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = self._pop_message(timeout=deadline - time.time())
            if msg is None:
                continue
            if predicate(msg):
                return msg
        raise TimeoutError("no matching DAP message received")
