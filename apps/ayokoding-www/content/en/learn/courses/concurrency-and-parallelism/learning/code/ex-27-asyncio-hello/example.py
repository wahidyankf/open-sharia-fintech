"""Example 27: Your First Coroutine -- `async def` and `asyncio.run`."""

import asyncio  # => co-26: single-threaded cooperative concurrency, driven by an event loop


async def greet(name: str) -> str:  # => `async def` marks this a COROUTINE FUNCTION, not a function
    await asyncio.sleep(0.05)  # => `await` suspends THIS coroutine, returning control to the loop
    return f"hello, {name}"  # => the coroutine's final result, once it resumes and returns


if __name__ == "__main__":  # => module entry point
    coro = greet("world")  # => calling greet() does NOT run its body yet -- it returns a coroutine OBJECT
    print(type(coro).__name__)  # => Output: coroutine
    message = asyncio.run(coro)  # => asyncio.run() creates an event loop, runs the coroutine TO COMPLETION
    print(message)  # => Output: hello, world

    # => `asyncio.run()` is the top-level entry point: it starts a fresh event loop, drives the
    # => coroutine through every `await` suspension point until it returns, then closes the loop.
    # => Calling greet() alone does nothing observable -- only actually AWAITING or RUNNING it does.
    assert message == "hello, world"  # => confirms the coroutine ran to completion and returned correctly
    print("ex-27 OK")  # => Output: ex-27 OK
