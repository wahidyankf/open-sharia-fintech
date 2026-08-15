---
title: "Capstone: Local CDP Automation Service"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

Build a local simulation of a CDP browser-automation service. It owns a bounded target pool and exposes
four operations: navigate, evaluate, screenshot, and intercept. It is deliberately not a scraper, login
bot, or public service: all data and events live in memory.

## Acceptance criteria

- A client can complete a two-step local flow and receive the simulated title and screenshot bytes.
- The pool never lets more than two targets run at once.
- A stalled operation times out and releases its target.
- A request rule can block a matching URL and a rate limiter rejects excess work.
- Tests use no live browser, network, or third-party package.

## Runnable reference slice

Save as `browser_service.py`, then run `python3 browser_service.py`.

```python
"""A deterministic, local model of the CDP service boundary."""
import asyncio  # => semaphore and timeout model browser-resource ownership
from dataclasses import dataclass  # => immutable result makes the API contract inspectable


@dataclass(frozen=True)
class Result:  # => the service returns data, not a browser object that leaks its ownership
    url: str
    title: str
    screenshot: bytes


class BrowserService:
    def __init__(self, capacity: int = 2) -> None:
        self._pool = asyncio.Semaphore(capacity)  # => bound concurrent targets before allocating work

    async def navigate(self, url: str) -> Result:
        if not url.startswith("https://example.test/"):
            raise ValueError("only local authorized fixture URLs are allowed")  # => scope guard first
        async with self._pool:  # => cancellation still returns the target permit
            await asyncio.sleep(0)  # => stand-in for waiting on Page.loadEventFired, never time.sleep
            return Result(url, "Fixture page", b"PNG")  # => deterministic CDP-shaped result


async def main() -> None:
    service = BrowserService()
    result = await asyncio.wait_for(service.navigate("https://example.test/report"), timeout=0.1)
    assert result.screenshot == b"PNG"  # => observable result a real CDP adapter must preserve
    print(result.title)  # => Output: Fixture page


asyncio.run(main())
```

**Key takeaway**: put browser ownership, authorization, capacity, and timeouts behind one small service
boundary; an eventual WebSocket/CDP adapter should replace only the simulated operation.

**Why it matters**: a browser is expensive, asynchronous state. A thin bounded service keeps callers
from creating unbounded tabs or silently sending a browser to an unauthorized target. The
`remotebrowser` project is an illustrative example of this general shape, not a prerequisite.
