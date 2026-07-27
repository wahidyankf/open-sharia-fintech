"""Example 71: Deadlock Detection via a Wait-For Graph."""
# A cycle in the wait-for graph (co-25) IS a deadlock -- no transaction in the cycle can ever proceed.


def has_cycle(
    wait_for: dict[int, int],
) -> list[int] | None:  # => co-25: DFS following each wait-for edge
    for start in (
        wait_for
    ):  # => try starting the cycle search from every transaction in the graph
        visited: list[int] = [
            start
        ]  # => the path built up so far, starting from this transaction
        current = wait_for.get(start)  # => who `start` is waiting for
        while (
            current is not None
        ):  # => keep following wait-for edges until a dead end OR a repeat
            if (
                current in visited
            ):  # => we have been here before on THIS path -- a cycle closed
                return visited[visited.index(current) :] + [
                    current
                ]  # => the exact cycle, as a list
            visited.append(current)  # => extend the path and keep following the chain
            current = wait_for.get(
                current
            )  # => who the NEXT transaction in the chain is waiting for
    return None  # => no cycle exists anywhere in the graph -- no deadlock


def choose_victim(
    cycle: list[int],
) -> int:  # => a simple, deterministic tie-breaker: the lowest txn_id
    return min(
        cycle
    )  # => aborting the lowest-id transaction is enough to break any cycle


wait_for = {
    1: 2,
    2: 3,
    3: 1,
}  # => txn 1 waits for txn 2, 2 waits for 3, and 3 waits back for 1 -- a cycle
cycle = has_cycle(
    wait_for
)  # => run the detector over this classic circular-wait scenario
print(cycle)  # => Output: [1, 2, 3, 1]

assert cycle is not None  # => a deadlock was correctly detected
victim = choose_victim(cycle)  # => pick which transaction to abort, breaking the cycle
print(victim)  # => Output: 1

assert victim in cycle  # => the chosen victim is genuinely part of the deadlock cycle
no_deadlock = has_cycle(
    {1: 2, 2: 3}
)  # => a plain wait CHAIN, not a cycle -- no deadlock here
assert (
    no_deadlock is None
)  # => confirms the detector does not false-positive on a non-circular wait
print("ex-71 OK")  # => Output: ex-71 OK
