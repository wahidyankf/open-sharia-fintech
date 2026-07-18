# pyright: strict
"""Example 68: A CRUD Workload -- the ORM Recommendation, With Rationale."""

from __future__ import annotations

from dataclasses import dataclass  # => a typed record for the workload's characteristics, not a loose dict


@dataclass(frozen=True)  # => co-27: immutable -- a workload description shouldn't mutate mid-decision
class Workload:  # => co-27: the SAME shape of record every choosing-tier example scores against
    name: str  # => a human label for what's being decided, e.g. "customer profile edit"
    is_object_shaped: bool  # => does the domain naturally look like objects with identity and relationships?
    is_set_oriented: bool  # => does the work aggregate/scan across MANY rows at once (reports, bulk jobs)?
    is_latency_critical: bool  # => does a single call need sub-millisecond, every-microsecond-counts overhead?


def choose_tier(w: Workload) -> tuple[str, str]:  # => co-27: returns (tier, rationale) -- a decision AND why
    if w.is_set_oriented:  # => co-25: set-oriented work belongs to raw SQL, regardless of anything else
        # => checked FIRST -- set-orientation overrides every other characteristic in this rubric
        return "raw_sql", "set-oriented workload -- aggregation belongs in the database, not a Python loop"
    if w.is_latency_critical:  # => co-27: hot paths avoid the ORM's per-object overhead even when object-shaped
        # => checked SECOND -- latency budget overrides object-shape once set-orientation is ruled out
        return "query_builder", "latency-critical -- skip identity-map/change-tracking overhead per call"
    if w.is_object_shaped:  # => co-06 + co-25: THIS is the ORM's sweet spot -- single-object CRUD, not set ops
        # => checked LAST among the "yes" branches -- only reached once the two override conditions are false
        return "orm", "single-entity CRUD on an object-shaped domain -- identity map + change tracking pay for themselves"
    # => the fallback -- none of the three signals fired, so default to the middle tier rather than either extreme
    return "query_builder", "default: composable, injection-safe SQL without paying for machinery you won't use"


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    crud = Workload(  # => co-27: a CONCRETE CRUD scenario -- editing one customer's profile fields
        name="customer profile edit",
        is_object_shaped=True,  # => a Customer with a name/email/address IS naturally an object
        is_set_oriented=False,  # => touches exactly ONE row per request, never a bulk scan
        is_latency_critical=False,  # => an admin-panel edit, not a request on the hot path
    )
    tier, rationale = choose_tier(crud)  # => co-27: runs the SAME rubric every choosing-tier example uses

    # => co-27: the rubric is a deliberate ORDERED decision tree, not a scoring/weighting scheme -- easy to reason about
    print(f"tier={tier}")  # => Output: tier=orm
    print(f"rationale={rationale}")  # => Output: rationale=single-entity CRUD on an object-shaped domain -- identity map + change tracking pay for themselves
    assert tier == "orm"  # => co-27: single-object CRUD on an object-shaped domain lands squarely on the ORM
    assert "identity map" in rationale or "change tracking" in rationale  # => the rationale names the SPECIFIC ORM feature that earns its keep
    # => co-27: swap ANY one characteristic and the decision changes -- set is_set_oriented=True and it becomes raw
    # => SQL (Example 69); set is_latency_critical=True and it drops to a query builder (Example 70) -- the tier
    # => follows from the workload's SHAPE, not from habit or which library the team already knows
    print("ex-68 OK")  # => Output: ex-68 OK
