"""Example 41: attaches to target.py, sets a breakpoint on its EARLY line, and reports whether
the breakpoint was reached before that line already ran."""

from __future__ import annotations

import pathlib
import sys

from dap_client import DapClient

TARGET_FILE = str(pathlib.Path(__file__).parent / "target.py")


def main() -> None:
    timeout = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
    client = DapClient("127.0.0.1", 15680)
    client.send("request", "initialize", {"clientID": "x", "adapterID": "debugpy"})
    client.wait_for(
        lambda m: m.get("command") == "initialize" and m.get("type") == "response"
    )
    client.send("request", "attach", {"justMyCode": False})
    client.wait_for(
        lambda m: m.get("type") == "event" and m.get("event") == "initialized"
    )
    client.send(
        "request",
        "setBreakpoints",
        {"source": {"path": TARGET_FILE}, "breakpoints": [{"line": 22}]},
    )
    client.wait_for(
        lambda m: m.get("command") == "setBreakpoints" and m.get("type") == "response"
    )
    client.send("request", "configurationDone")
    client.wait_for(
        lambda m: m.get("command") == "attach" and m.get("type") == "response"
    )
    try:
        stopped = client.wait_for(
            lambda m: m.get("type") == "event" and m.get("event") == "stopped",
            timeout=timeout,
        )
        print("RESULT: breakpoint HIT -- stopped reason:", stopped["body"]["reason"])
        tid = stopped["body"]["threadId"]
        client.send("request", "continue", {"threadId": tid})
    except TimeoutError:
        print(
            "RESULT: breakpoint NEVER hit -- the line already ran before this client could attach"
        )


if __name__ == "__main__":
    main()
