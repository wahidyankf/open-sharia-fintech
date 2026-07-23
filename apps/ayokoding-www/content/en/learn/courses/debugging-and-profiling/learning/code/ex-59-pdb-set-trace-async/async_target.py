"""Example 59: pdb.set_trace_async() (Python 3.14+, PEP 768-based) -- an async-aware
breakpoint usable directly inside a coroutine at an `await` point.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to async breakpoints itself

import asyncio  # => co-01: the coroutine runtime pdb.set_trace_async() is specifically designed to pause inside
import pdb  # => co-01/co-06: set_trace_async() is new in 3.14 -- pdb.set_trace() alone cannot safely await


async def fetch_item(
    item_id: int,
) -> int:  # => co-01: a coroutine, not a plain function -- awaits are legal inside
    await asyncio.sleep(
        0.01
    )  # => co-01: a real await point BEFORE the breakpoint -- simulates genuine async I/O
    await pdb.set_trace_async()  # =>  co-01/co-06: an async-native breakpoint
    return (
        item_id * 10
    )  # => co-01: runs only AFTER the debugger session releases control (pdb `c`)


async def main() -> (
    None
):  # => co-01: the coroutine that awaits fetch_item(), one frame above the breakpoint
    result = await fetch_item(
        item_id=7
    )  # => co-01: a fixed input -- reproducible across runs
    print(
        f"result: {result}"
    )  # => co-01: prints only after the paused coroutine's Task resumes and completes


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    asyncio.run(
        main()
    )  # => co-01: the ONE call that starts the event loop and reaches the async breakpoint
