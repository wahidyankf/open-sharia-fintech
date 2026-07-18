"""Kata 6 (after): asyncio.sleep() yields control -- the quick coroutine now overlaps and finishes first."""

import asyncio


async def slow_report(log: list[str]) -> None:
    log.append("report: started")
    await asyncio.sleep(0.3)  # FIX: a COOPERATIVE sleep -- suspends only THIS coroutine
    log.append("report: finished")


async def quick_ping(log: list[str]) -> None:
    log.append("ping: started")
    await asyncio.sleep(0.05)  # => the event loop is free to run this while slow_report is suspended
    log.append("ping: finished")


async def main() -> list[str]:
    log: list[str] = []
    await asyncio.gather(slow_report(log), quick_ping(log))
    return log


result = asyncio.run(main())
print(result)
# FIX: both coroutines start immediately (neither blocks the OS thread), and since quick_ping's
# 0.05s await is far shorter than slow_report's 0.3s await, quick_ping finishes FIRST -- true
# cooperative overlap, exactly what asyncio.gather is supposed to provide.
assert result == ["report: started", "ping: started", "ping: finished", "report: finished"]
print("kata OK (fix verified: the faster coroutine finished first, as intended)")
