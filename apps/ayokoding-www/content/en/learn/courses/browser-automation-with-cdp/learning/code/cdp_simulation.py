"""Local, deterministic CDP-shaped simulations for this course.

Run one named scenario with: python3 cdp_simulation.py <scenario>
The program intentionally opens no browser or network connection.
"""

# => asyncio models CDP's asynchronous command/event boundary with the standard library.
import asyncio  # => the simulator yields exactly as a real awaited event would yield.

# => json models the message representation, not a dependency or a browser transport.
import json  # => CDP messages are JSON objects on a WebSocket in a real adapter.

# => sys receives the example-selected scenario without an application framework.
import sys  # => this keeps each invocation runnable with Python alone.


async def simulate(name: str) -> dict[str, object]:
    # => keep the command shape explicit so readers can see the correlation boundary.
    command = {"id": 1, "method": "Course.simulate", "params": {"scenario": name}}
    # => Command id gives a future real response an unambiguous correlation key.
    # => yield like an awaited CDP event; a blocking sleep would hide scheduling behavior.
    await asyncio.sleep(0)  # => no elapsed delay is guessed by this safe simulation.
    # => construct a response after the yield, as an event loop would resume a future.
    result = {"id": command["id"], "result": {"scenario": name, "safe": True}}
    # => The simulation has a response-shaped value and no browser side effects.
    # => correlation is the invariant that lets concurrent requests share one transport safely.
    assert (
        result["id"] == command["id"]
    )  # => response id must equal the originating command id.
    return result


def main() -> None:
    # => choose a named course scenario while retaining a useful default for direct execution.
    scenario = sys.argv[1] if len(sys.argv) == 2 else "first-command"
    # => own one short-lived loop; a service adapter would own this loop for its lifetime instead.
    response = asyncio.run(
        simulate(scenario)
    )  # => own one short-lived event loop for this example.
    # => sorted JSON is stable, so each mapped example has a deterministic assertion surface.
    print(
        json.dumps(response, sort_keys=True)
    )  # => Output is deterministic and safe to assert in CI.


if __name__ == "__main__":
    # => direct execution invokes the same entry point every example command references.
    main()
