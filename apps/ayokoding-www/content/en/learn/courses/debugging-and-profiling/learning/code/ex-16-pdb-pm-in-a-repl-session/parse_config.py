"""Example 16: pdb.pm() in a REPL Session."""

from __future__ import annotations

import sys


def parse_port(config: dict[str, str]) -> int:
    raw_port = config["port"]  # the SAME case-sensitivity bug as Example 15
    return int(raw_port)


settings = {"HOST": "localhost", "PORT": "8080"}
try:
    print(parse_port(settings))
except Exception as exc:
    # A real interactive REPL does this automatically for every uncaught exception (sys.last_exc
    # since Python 3.12, plus the older sys.last_type/value/traceback trio for compatibility) --
    # this line reproduces that same REPL behavior so pdb.pm() below has something to attach to,
    # without needing an actual re-run of the program (co-04's whole point: no restart).
    sys.last_exc = exc
    sys.last_type, sys.last_value, sys.last_traceback = sys.exc_info()
    print(f"{type(sys.last_value).__name__}: {sys.last_value}")
