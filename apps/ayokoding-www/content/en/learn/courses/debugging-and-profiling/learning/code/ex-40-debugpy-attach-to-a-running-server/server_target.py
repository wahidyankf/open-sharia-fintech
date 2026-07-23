"""Example 40: debugpy: Attach to a Running Server -- the target process."""

from __future__ import annotations

import time

import debugpy

debugpy.listen(
    ("127.0.0.1", 15679)
)  # co-06: opens a DAP listener -- the process keeps running
print("debugpy listening on 15679", flush=True)


def handle_request(request_id: int) -> int:
    computed = (
        request_id * 2
    )  # the line this example's breakpoint lands on, mid-request
    return computed


def main() -> None:
    request_id = 0
    while request_id < 20:
        request_id += 1
        result = handle_request(request_id)
        print(f"handled request_id={request_id} result={result}", flush=True)
        time.sleep(0.3)


main()
