"""Example 16: When to Pick NoSQL: a Checklist."""  # => co-02: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-02: a typed record for one workload's own three deciding factors


@dataclass(frozen=True)  # => frozen -- a workload's stated shape should not be silently mutated after scoring
class Workload:  # => co-02: the three factors this checklist actually weighs
    name: str  # => a human-readable label for the workload
    predictable_access_pattern: bool  # => co-02: can the queries be enumerated in advance, not ad hoc joins?
    needs_horizontal_scale: bool  # => co-02: does write volume exceed one node's own capacity?
    tolerates_eventual_consistency: bool  # => co-02: can the app accept a briefly stale read for that speed/scale?


def recommend(workload: Workload) -> str:  # => co-02: scores a workload and returns "relational" or "NoSQL"
    """Score a workload against the three-factor checklist and return a recommendation."""  # => documents the contract
    score = sum(
        [  # => co-02: each TRUE factor is one point toward "NoSQL fits this workload"
            workload.predictable_access_pattern,  # => factor 1: queries known in advance, not ad hoc?
            workload.needs_horizontal_scale,  # => factor 2: does write volume outgrow one node?
            workload.tolerates_eventual_consistency,  # => factor 3: can reads be briefly stale?
        ]
    )  # => bool sums as 0 or 1 in Python -- 3 true factors sums to 3
    return "NoSQL" if score >= 2 else "relational"  # => co-02: a simple majority-of-three threshold, stated up front


SESSION_CACHE = Workload(  # => co-02: workload 1 -- ephemeral session tokens at high write volume
    name="session cache",
    predictable_access_pattern=True,
    needs_horizontal_scale=True,
    tolerates_eventual_consistency=True,  # => all 3 factors True
)  # => 3/3 factors True -- the checklist's own textbook "obviously NoSQL" case
ORDER_LEDGER = Workload(  # => co-02: workload 2 -- financial ledger needing joins and strict consistency
    name="order ledger with ad hoc reporting joins",  # => the name alone signals unpredictable, join-heavy access
    predictable_access_pattern=False,  # => ad hoc reporting joins are the OPPOSITE of a known access pattern
    needs_horizontal_scale=False,  # => a ledger's write volume fits comfortably on one strongly-consistent node
    tolerates_eventual_consistency=False,  # => a financial balance must never read stale -- strict consistency required
)  # => 0/3 factors True -- the checklist's own textbook "stay relational" case


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for workload in (SESSION_CACHE, ORDER_LEDGER):  # => co-02: runs the SAME checklist against both sample workloads
        recommendation = recommend(workload)  # => scores this one workload
        print(f"{workload.name}: {recommendation}")  # => Output: session cache: NoSQL / order ledger with ad hoc reporting joins: relational
    assert recommend(SESSION_CACHE) == "NoSQL"  # => co-02: 3/3 factors favor NoSQL -- high-throughput, predictable, tolerant
    assert recommend(ORDER_LEDGER) == "relational"  # => co-02: 0/3 factors favor NoSQL -- needs joins and strong consistency


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
