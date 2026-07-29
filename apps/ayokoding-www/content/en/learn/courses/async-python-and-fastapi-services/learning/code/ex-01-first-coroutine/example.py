"""Example 1: First Coroutine via asyncio Run."""

# => asyncio is the standard-library event loop -- no third-party package is needed (co-02)
import asyncio  # => the module that owns the loop, coroutines, Tasks, and gather


async def greet() -> str:  # => "async def" makes this a COROUTINE, not a normal function (co-01)
    # => calling greet() does NOT run the body -- it returns a coroutine OBJECT you must schedule
    await asyncio.sleep(0.01)  # => await SUSPENDS greet, handing control back to the loop for ~10ms
    # => while suspended the loop is free to run OTHER coroutines -- that is the whole point (co-02)
    return "hello from a coroutine"  # => the value the awaiter receives once this completes


def main() -> None:  # => a plain (non-async) entry point -- the bridge into the async world
    # => asyncio.run creates a FRESH event loop, runs one coroutine to completion, then closes it
    message = asyncio.run(greet())  # => the ONLY correct top-level driver for a coroutine (co-01)
    print(message)  # => Output: hello from a coroutine


if __name__ == "__main__":  # => only runs when executed directly, not on import
    main()  # => drives the coroutine via asyncio.run
