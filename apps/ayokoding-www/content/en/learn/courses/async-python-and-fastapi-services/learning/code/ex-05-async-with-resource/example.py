"""Example 5: Managing a Resource with async with."""

import asyncio  # => the event-loop module (co-02)


class AsyncConnection:  # => models a resource whose acquire/release themselves need to await (co-05)
    async def __aenter__(self) -> "AsyncConnection":  # => async context-manager ENTRY -- runs on "async with"
        await asyncio.sleep(0.01)  # => simulate an async "connect" that yields to the loop
        print("opened")  # => confirms setup ran
        return self  # => the bound resource handed to the "as" name

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:  # => EXIT -- runs on block exit
        await asyncio.sleep(0.01)  # => simulate an async "close" that yields to the loop
        print("closed")  # => confirms teardown ran even if the body raised


async def main() -> None:  # => demonstrates the setup/body/teardown order
    async with AsyncConnection() as conn:  # => __aenter__ runs, then the body, then __aexit__ (co-05)
        _ = conn  # => the live resource is available only INSIDE the block
        print("using")  # => body runs between "opened" and "closed"


if __name__ == "__main__":  # => only runs when executed directly
    asyncio.run(main())  # => Output order: opened / using / closed
