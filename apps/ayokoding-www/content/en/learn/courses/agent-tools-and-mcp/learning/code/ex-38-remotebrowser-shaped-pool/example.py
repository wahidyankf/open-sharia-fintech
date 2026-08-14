# A semaphore represents bounded browser-like capacity.
import asyncio

# Two permits are the provider's fixed concurrency budget.
pool = asyncio.Semaphore(2)


# Work must acquire a permit before it can run.
async def task() -> str:
    # Context management releases permits even after failure.
    async with pool:
        return "served"


# Two local tasks fit the configured capacity.
assert asyncio.run(task()) == "served"
# Print the bounded-service observation.
print("served")
