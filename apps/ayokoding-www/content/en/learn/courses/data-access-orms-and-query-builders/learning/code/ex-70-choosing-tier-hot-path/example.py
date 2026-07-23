# pyright: strict
"""Example 70: A Hot-Path Workload -- the Query-Builder/Raw Recommendation, With Rationale."""

from __future__ import annotations

from dataclasses import dataclass  # => a typed record for the workload's characteristics, not a loose dict


@dataclass(frozen=True)  # => co-27: immutable -- a workload description shouldn't mutate mid-decision
class Workload:  # => co-27: the SAME shape of record every choosing-tier example scores against (see Example 68)
    name: str  # => a human label for what's being decided, e.g. "product-lookup API endpoint"
    is_object_shaped: bool  # => does the domain naturally look like objects with identity and relationships?
    is_set_oriented: bool  # => does the work aggregate/scan across MANY rows at once (reports, bulk jobs)?
    is_latency_critical: bool  # => does a single call need sub-millisecond, every-microsecond-counts overhead?


def choose_tier(w: Workload) -> tuple[str, str]:  # => co-27: the SAME ordered rubric as Examples 68/69 -- reused unchanged
    if w.is_set_oriented:  # => co-25: checked FIRST -- set-orientation overrides every other characteristic
        # => never reached for THIS workload -- a hot-path lookup touches one or a few rows, not a full scan
        return "raw_sql", "set-oriented workload -- aggregation belongs in the database, not a Python loop"
    if w.is_latency_critical:  # => checked SECOND -- latency budget overrides object-shape once ruled out above
        # => this branch is exactly why THIS example's workload lands on a query builder, not the ORM
        return "query_builder", "latency-critical -- skip identity-map/change-tracking overhead per call"
    if w.is_object_shaped:  # => checked LAST among the "yes" branches -- the ORM's sweet spot, not reached here
        # => never reached for THIS workload -- the latency check above already returned
        return "orm", "single-entity CRUD on an object-shaped domain -- identity map + change tracking pay for themselves"
    # => the fallback -- unreachable for this workload, since the SECOND branch already returned
    return "query_builder", "default: composable, injection-safe SQL without paying for machinery you won't use"


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    hot_path = Workload(  # => co-27: a CONCRETE hot-path scenario -- a product-lookup API endpoint under heavy load
        name="product-lookup API endpoint",
        is_object_shaped=True,  # => a Product IS naturally an object -- this does NOT decide the tier alone
        is_set_oriented=False,  # => fetches ONE product per call, never a bulk scan
        is_latency_critical=True,  # => co-27: called thousands of times per second -- per-call overhead compounds
    )
    tier, rationale = choose_tier(hot_path)  # => co-27: runs the SAME rubric as every choosing-tier example

    # => co-27: three examples (68/69/70), one rubric -- reproducible decisions beat "the team already knows the ORM"
    print(f"tier={tier}")  # => Output: tier=query_builder
    print(f"rationale={rationale}")  # => Output: rationale=latency-critical -- skip identity-map/change-tracking overhead per call
    assert tier == "query_builder"  # => co-27: latency-critical wins over object-shape -- object-shape alone is NOT sufficient
    assert "latency" in rationale or "overhead" in rationale  # => the rationale names the SPECIFIC reason, not a vague preference
    # => co-27: THIS is the pairwise contrast with Example 68 -- identical `is_object_shaped=True`, but flipping
    # => `is_latency_critical` to True changes the recommendation from "orm" to "query_builder"; the ORM's identity
    # => map and change tracking are real per-call costs, worth paying for CRUD convenience but not on a hot path
    print("ex-70 OK")  # => Output: ex-70 OK
