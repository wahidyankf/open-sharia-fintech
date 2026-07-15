"""Example 40: a minimal DAP client -- attaches to server_target.py while it is ALREADY running,
sets a breakpoint on a live request handler, and inspects a local variable at the stop."""

from __future__ import annotations

import pathlib

from dap_client import DapClient

TARGET_FILE = str(pathlib.Path(__file__).parent / "server_target.py")


def main() -> None:
    client = DapClient("127.0.0.1", 15679)
    client.send(
        "request",
        "initialize",
        {"clientID": "manual-dap-client", "adapterID": "debugpy"},
    )
    client.wait_for(
        lambda m: m.get("type") == "response" and m.get("command") == "initialize"
    )

    client.send(
        "request", "attach", {"justMyCode": False}
    )  # co-06: attaches to the LIVE process
    client.wait_for(
        lambda m: m.get("type") == "event" and m.get("event") == "initialized"
    )

    client.send(
        "request",
        "setBreakpoints",
        {"source": {"path": TARGET_FILE}, "breakpoints": [{"line": 14}]},
    )
    bp_resp = client.wait_for(
        lambda m: m.get("type") == "response" and m.get("command") == "setBreakpoints"
    )
    print("breakpoints verified:", bp_resp["body"]["breakpoints"])

    client.send("request", "configurationDone")
    attach_resp = client.wait_for(
        lambda m: m.get("type") == "response" and m.get("command") == "attach"
    )
    print("attach response success:", attach_resp["success"])

    stopped = client.wait_for(
        lambda m: m.get("type") == "event" and m.get("event") == "stopped", timeout=15
    )
    print("stopped event reason:", stopped["body"]["reason"])
    thread_id = stopped["body"]["threadId"]

    client.send("request", "stackTrace", {"threadId": thread_id})
    stack = client.wait_for(
        lambda m: m.get("type") == "response" and m.get("command") == "stackTrace"
    )
    frame_id = stack["body"]["stackFrames"][0]["id"]
    print("top frame name:", stack["body"]["stackFrames"][0]["name"])

    client.send("request", "scopes", {"frameId": frame_id})
    scopes = client.wait_for(
        lambda m: m.get("type") == "response" and m.get("command") == "scopes"
    )
    locals_ref = next(s for s in scopes["body"]["scopes"] if s["name"] == "Locals")[
        "variablesReference"
    ]

    client.send("request", "variables", {"variablesReference": locals_ref})
    variables = client.wait_for(
        lambda m: m.get("type") == "response" and m.get("command") == "variables"
    )
    for v in variables["body"]["variables"]:
        print(f"local: {v['name']} = {v['value']}")

    client.send("request", "continue", {"threadId": thread_id})
    print("continued")


if __name__ == "__main__":
    main()
