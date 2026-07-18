# pyright: strict
"""Example 69: An Analytics Workload -- the Raw-SQL Recommendation, With Rationale."""

from __future__ import annotations

from dataclasses import dataclass  # => a typed record for the workload's characteristics, not a loose dict


@dataclass(frozen=True)  # => co-27: immutable -- a workload description shouldn't mutate mid-decision
class Workload:  # => co-27: the SAME shape of record every choosing-tier example scores against (see Example 68)
    name: str  # => a human label for what's being decided, e.g. "monthly revenue report"
    is_object_shaped: bool  # => does the domain naturally look like objects with identity and relationships?
    is_set_oriented: bool  # => does the work aggregate/scan across MANY rows at once (reports, bulk jobs)?
    is_latency_critical: bool  # => does a single call need sub-millisecond, every-microsecond-counts overhead?


def choose_tier(w: Workload) -> tuple[str, str]:  # => co-27: the SAME ordered rubric as Example 68 -- reused unchanged
    if w.is_set_oriented:  # => co-25: checked FIRST -- set-orientation overrides every other characteristic
        # => this branch is exactly why THIS example's workload lands on raw SQL, not the other two branches
        return "raw_sql", "set-oriented workload -- aggregation belongs in the database, not a Python loop"
    if w.is_latency_critical:  # => checked SECOND -- latency budget overrides object-shape once ruled out above
        # => never reached for THIS workload -- the set-oriented check above already returned
        return "query_builder", "latency-critical -- skip identity-map/change-tracking overhead per call"
    if w.is_object_shaped:  # => checked LAST among the "yes" branches -- the ORM's sweet spot, not reached here
        # => never reached for THIS workload either -- an analytics report is never object-shaped
        return "orm", "single-entity CRUD on an object-shaped domain -- identity map + change tracking pay for themselves"
    # => the fallback -- unreachable for this workload, since the FIRST branch already returned
    return "query_builder", "default: composable, injection-safe SQL without paying for machinery you won't use"


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    analytics = Workload(  # => co-27: a CONCRETE analytics scenario -- a monthly revenue-by-region report
        name="monthly revenue report",
        is_object_shaped=False,  # => a GROUP BY total is a NUMBER, not an object with identity
        is_set_oriented=True,  # => co-25: scans and aggregates potentially millions of order rows at once
        is_latency_critical=False,  # => a scheduled batch report, not a request on the hot path
    )
    tier, rationale = choose_tier(analytics)  # => co-27: runs the SAME rubric as every choosing-tier example

    # => co-27: the SAME ordered rubric, a DIFFERENT workload -- this is what makes the decision reproducible, not ad hoc
    print(f"tier={tier}")  # => Output: tier=raw_sql
    print(f"rationale={rationale}")  # => Output: rationale=set-oriented workload -- aggregation belongs in the database, not a Python loop
    assert tier == "raw_sql"  # => co-27: a set-oriented report lands on raw SQL, REGARDLESS of the other two flags
    assert "aggregation" in rationale or "set-oriented" in rationale  # => the rationale names the SPECIFIC reason, not a vague preference
    # => co-27: notice `is_object_shaped=False` never even gets EVALUATED -- `is_set_oriented=True` short-circuits
    # => the rubric at the FIRST check; Example 65 showed the concrete cost of ignoring this signal -- loading every
    # => row into Python objects just to sum them in a for-loop, work Postgres' own GROUP BY does in one pass
    print("ex-69 OK")  # => Output: ex-69 OK
