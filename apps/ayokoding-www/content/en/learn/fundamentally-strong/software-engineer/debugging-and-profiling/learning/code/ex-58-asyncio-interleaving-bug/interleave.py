"""Example 58: a check-then-act race on a shared dict across two coroutines,
forced to interleave with an explicit asyncio.sleep(0) yield.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the race itself

import asyncio  # => co-20: the SINGLE-threaded concurrency model this example's race lives inside

shared_inventory: dict[str, int] = {"widget": 1}  # =>  only ONE widget in stock


async def reserve_if_available(
    coroutine_name: str, results: list[str]
) -> None:  # => co-20: runs as TWO concurrent coroutines
    # co-20: CLASSIC check-then-act -- the check and the act are two separate
    # awaits apart, so another coroutine can run in between on a single thread.
    if (
        shared_inventory["widget"] > 0
    ):  # => co-20: the CHECK -- both coroutines can see stock=1 before either acts
        await asyncio.sleep(0)  # =>  force a real yield to the event loop HERE
        shared_inventory["widget"] -= (
            1  # => co-20: the ACT -- happens AFTER the yield, so it can race with the other coroutine
        )
        results.append(
            f"{coroutine_name}: RESERVED (stock now {shared_inventory['widget']})"
        )  # => co-20: records the outcome
    else:  # => co-20: the branch neither coroutine should take, given only ONE widget and TWO reservers
        results.append(
            f"{coroutine_name}: DENIED (out of stock)"
        )  # => co-20: the CORRECT outcome for a second caller


async def run_once() -> list[
    str
]:  # => co-20: one full attempt -- resets stock, then races two coroutines
    shared_inventory["widget"] = 1  # =>  reset for each run
    results: list[
        str
    ] = []  # => co-20: collects each coroutine's own outcome string, in completion order
    await asyncio.gather(  # => co-20: schedules BOTH coroutines onto the SAME single-threaded event loop
        reserve_if_available(
            "coro-A", results
        ),  # => co-20: the FIRST reserver -- races coro-B for the one widget
        reserve_if_available(
            "coro-B", results
        ),  # => co-20: the SECOND reserver -- races coro-A for the SAME widget
    )  # => co-20: gather() returns once BOTH coroutines have completed
    return results  # => co-20: whatever both coroutines recorded, in whichever order they actually finished


async def main() -> (
    None
):  # => co-20: runs the race 20 times and reports how often overselling actually happens
    failures = 0  # => co-20: tallies how many of the 20 runs actually oversold the single widget
    for run_idx in range(
        20
    ):  # => co-20: 20 independent attempts -- the forced yield makes this reliable, not rare
        results = (
            await run_once()
        )  # => co-20: one fresh shared_inventory state and two fresh coroutines
        reserved_count = sum(
            1 for r in results if "RESERVED" in r
        )  # => co-20: counts how many actually reserved
        if (
            reserved_count > 1
        ):  # => co-20: MORE than one reservation for ONE widget is the overselling bug
            failures += (
                1  # => co-20: counts this run as a demonstrated interleaving bug
            )
            print(
                f"run {run_idx}: BOTH coroutines reserved! final stock={shared_inventory['widget']} -- {results}"
            )  # => co-20
    print(
        f"summary: {failures}/20 runs show the overselling bug (both coroutines reserved the same single widget)"
    )  # => co-20
    assert failures >= 1, (
        "expected the forced yield to reliably reproduce the overselling race"
    )  # => co-20: the real check
    print(
        "confirmed: forcing the yield with asyncio.sleep(0) makes the interleaving bug reproducible"
    )  # => co-20


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    asyncio.run(
        main()
    )  # => co-20: the ONE call that starts the event loop and drives all 20 attempts
