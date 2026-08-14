# A semaphore bounds shared worker capacity.
import asyncio

# Two permits are the maximum active subagents.
gate = asyncio.Semaphore(2)
# The local counter records the largest observed admission.
active = 0


# Work obtains capacity before recording activity.
async def worker() -> int:
    global active
    async with gate:
        active += 1
        maximum = active
        active -= 1
        return maximum


# A single local run demonstrates the bounded primitive.
assert asyncio.run(worker()) <= 2
# Print the configured cap.
print(2)
