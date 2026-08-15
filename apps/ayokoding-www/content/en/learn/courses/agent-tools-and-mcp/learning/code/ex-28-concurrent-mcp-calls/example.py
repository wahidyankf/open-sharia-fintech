# Asyncio models independent local MCP calls.
import asyncio


# Each call returns a typed named observation.
async def call(name: str) -> tuple[str, str]:
    # Yield once to make concurrent scheduling observable.
    await asyncio.sleep(0)
    # Return the provider-owned result.
    return name, f"result:{name}"


# The main coroutine merges correlated results.
async def main() -> dict[str, str]:
    # Gather retains each call's result position.
    pairs = await asyncio.gather(call("a"), call("b"))
    # Names become stable merge keys.
    return dict(pairs)


# The local run requires no remote providers.
result = asyncio.run(main())
# Both observations survive the merge.
assert result == {"a": "result:a", "b": "result:b"}
# Print the merged map.
print(result)
