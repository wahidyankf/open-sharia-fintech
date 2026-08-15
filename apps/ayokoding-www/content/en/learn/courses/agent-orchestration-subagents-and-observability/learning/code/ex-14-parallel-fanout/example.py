# Asyncio models independent subagent work.
import asyncio


# A worker yields once before returning its own name.
async def worker(name: str) -> str:
    await asyncio.sleep(0)
    return name


# A coroutine owns gather before the top-level runner starts.
async def fanout() -> list[str]:
    # Gather joins independently scheduled workers.
    return await asyncio.gather(worker("a"), worker("b"), worker("c"))


# The runner executes the complete local orchestration coroutine.
result = asyncio.run(fanout())
# Every fan-out result returns to the coordinator.
assert result == ["a", "b", "c"]
# Print the joined results.
print(result)
