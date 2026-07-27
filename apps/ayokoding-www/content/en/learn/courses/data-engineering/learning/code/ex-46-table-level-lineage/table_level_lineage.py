"""Worked Example 46: Table-Level Lineage."""  # => co-19: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

LINEAGE_EDGES = [  # => co-19: dataset -> dataset edges -- OpenLineage's own table-level answer to "does X feed Y"
    ("bronze_orders", "silver_orders"),  # => co-19: bronze feeds silver
    ("silver_orders", "gold_region_totals"),  # => co-19: silver feeds gold
    ("silver_orders", "gold_customer_ltv"),  # => co-19: silver ALSO feeds a second gold table
]  # => co-19: closes LINEAGE_EDGES -- a small, invented lineage graph, three edges across four datasets


def downstream_of(dataset: str, edges: list[tuple[str, str]]) -> set[str]:  # => co-19: transitive downstream discovery -- BFS over the edge list
    """Return every dataset transitively fed BY `dataset`, following edges to any depth."""  # => co-19: documents downstream_of's contract -- no runtime output, just sets its __doc__
    discovered: set[str] = set()  # => co-19: every dataset found downstream so far
    frontier = [dataset]  # => co-19: the BFS frontier -- starts at the queried dataset itself
    while frontier:  # => co-19: keep expanding until no new downstream dataset is found
        current = frontier.pop()  # => co-19: take one dataset off the frontier
        for upstream, downstream in edges:  # => co-19: scan every edge for one starting AT the current dataset
            if upstream == current and downstream not in discovered:  # => co-19: a NEW downstream dataset, not yet discovered
                discovered.add(downstream)  # => co-19: record it as downstream
                frontier.append(downstream)  # => co-19: and continue the search FROM it too -- transitive, not just one hop
    return discovered  # => co-19: returns this computed value to the caller


if __name__ == "__main__":  # => co-19: entry point -- runs only when this file executes directly, not on import
    changed_table = "bronze_orders"  # => co-19: imagine this table's schema just changed -- what's affected?
    affected = downstream_of(changed_table, LINEAGE_EDGES)  # => co-19: everything transitively fed by the changed table
    print(f"If {changed_table!r} changes, transitively affected datasets: {sorted(affected)}")  # => co-19: prints the full blast radius

    expected_affected = {"silver_orders", "gold_region_totals", "gold_customer_ltv"}  # => co-19: ALL three downstream datasets, not just the direct child
    print(f"Discovered set matches expected transitive downstream: {affected == expected_affected}")  # => co-19: prints the exact-match check
    assert affected == expected_affected, "table-level lineage must discover EVERY transitively downstream dataset"  # => co-19: the claim
    print(f"MATCH: {changed_table!r}'s change reaches {len(affected)} downstream datasets, two hops away included")  # => co-19
    # => co-19: table-level lineage answers "does X feed Y" -- it says nothing about WHICH columns, which ex-47 covers next
