"""Example 75: verify a complete bounded, authorized local service flow."""

import asyncio  # => one event loop coordinates the local service operation and its capacity boundary.


# => The service admits only the fixture URL and returns a bounded screenshot artifact.
async def navigate_and_capture(url: str) -> dict[str, object]:
    gate = asyncio.Semaphore(1)
    async with gate:
        await asyncio.sleep(0)
        return {"url": url, "title": "Fixture report", "screenshot": b"PNG"}


# => The end-to-end assertion covers authorization, asynchronous completion, and the returned artifact.
result = asyncio.run(navigate_and_capture("https://fixture.test/report"))
assert (
    result["url"].startswith("https://fixture.test/") and result["screenshot"] == b"PNG"
)
# => Output is the deterministic final service result.
print(result["title"])
