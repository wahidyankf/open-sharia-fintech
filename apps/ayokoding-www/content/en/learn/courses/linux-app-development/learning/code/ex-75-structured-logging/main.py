"""Emit a structured JSON lifecycle log record."""

import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.info(
    json.dumps({"event": "status_request", "socket": "notes.sock", "result": "ok"})
)
