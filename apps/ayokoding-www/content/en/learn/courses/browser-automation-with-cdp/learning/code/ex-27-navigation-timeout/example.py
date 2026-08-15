"""Example 27: bound a navigation with an asyncio deadline."""

import asyncio  # => asyncio supplies cancellable deadlines without blocking the event loop.


# => The fixture navigation yields once, like a page waiting for a lifecycle event.
async def navigate() -> str:
    await asyncio.sleep(0)
    return "loaded"


# => The deadline converts an unbounded wait into a typed, observable result.
assert asyncio.run(asyncio.wait_for(navigate(), timeout=0.1)) == "loaded"
# => Output confirms the local navigation completed before its deadline.
print("navigation completed within deadline")
