"""Kata 6 (before): a blocking time.sleep() inside one coroutine freezes the ENTIRE event loop."""

import asyncio
import time


async def slow_report(log: list[str]) -> None:
    log.append("report: started")
    time.sleep(0.3)  # SMELL: BLOCKING sleep -- holds the entire OS thread, not just this coroutine
    log.append("report: finished")


async def quick_ping(log: list[str]) -> None:
    log.append("ping: started")
    await asyncio.sleep(0.05)  # => a genuinely cooperative sleep -- SHOULD finish long before the report
    log.append("ping: finished")


async def main() -> list[str]:
    log: list[str] = []
    await asyncio.gather(slow_report(log), quick_ping(log))  # => scheduled to run "concurrently"
    return log


result = asyncio.run(main())
print(result)
# BUG: slow_report() never hits an `await` between its two log lines, so once its task starts
# running it holds the ONE OS thread the event loop runs on for the FULL 0.3s -- quick_ping()'s
# task cannot even START until slow_report() finishes completely, even though quick_ping() only
# needs 0.05s. "ping: started" ends up AFTER "report: finished", not overlapped as intended.
assert result == ["report: started", "report: finished", "ping: started", "ping: finished"]
print("kata OK (bug reproduced: the faster coroutine never got a chance to overlap)")
