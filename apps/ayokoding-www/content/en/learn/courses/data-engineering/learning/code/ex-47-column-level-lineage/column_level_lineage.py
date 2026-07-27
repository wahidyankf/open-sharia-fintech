"""Worked Example 47: Column-Level Lineage."""  # => co-19: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

COLUMN_LINEAGE_EDGES = [  # => co-19: input_column -> output_column edges, each tagged with the transform that produced it
    ("silver_orders.amount", "gold_region_totals.total_amount", "SUM"),  # => co-19: aggregated via SUM
    ("silver_orders.region", "gold_region_totals.region", "GROUP BY"),  # => co-19: passed through as a grouping key
    ("silver_orders.customer_id", "gold_customer_ltv.customer_id", "GROUP BY"),  # => co-19: a DIFFERENT output table entirely
    ("silver_orders.amount", "gold_customer_ltv.lifetime_value", "SUM"),  # => co-19: the SAME input column feeds a SECOND output column
]  # => co-19: closes COLUMN_LINEAGE_EDGES -- OpenLineage's own column-level answer to "which input produced which output"


def inputs_feeding(output_column: str, edges: list[tuple[str, str, str]]) -> list[tuple[str, str]]:  # => co-19: impact analysis, one output at a time
    """Return every (input_column, transform) pair that feeds `output_column`."""  # => co-19: documents inputs_feeding's contract -- no runtime output, just sets its __doc__
    return [(inp, transform) for inp, out, transform in edges if out == output_column]  # => co-19: filter to edges landing AT this exact output


if __name__ == "__main__":  # => co-19: entry point -- runs only when this file executes directly, not on import
    target_output = "gold_region_totals.total_amount"  # => co-19: "which input column produced THIS specific output column?"
    feeding_inputs = inputs_feeding(target_output, COLUMN_LINEAGE_EDGES)  # => co-19: run the impact-analysis query
    print(f"Inputs feeding {target_output!r}: {feeding_inputs}")  # => co-19: prints exactly which input column(s) and transform(s)

    same_input_multiple_outputs = [  # => co-19: the SAME input column, silver_orders.amount, feeds TWO different output columns
        out  # => co-19: the output column name projected for each matching edge
        for inp, out, _ in COLUMN_LINEAGE_EDGES  # => co-19: iterate every edge, unpacking (input, output, transform) -- transform discarded via _
        if inp == "silver_orders.amount"  # => co-19: filters to edges STARTING at this exact input column, discarding the transform label
    ]  # => co-19: shows column-level lineage's extra precision over table-level -- WHICH column, not just WHICH table
    print(f"Output columns fed by silver_orders.amount: {sorted(same_input_multiple_outputs)}")  # => co-19: prints both dependents

    assert feeding_inputs == [("silver_orders.amount", "SUM")], "the exact one input column + transform feeding this output"  # => co-19
    assert set(same_input_multiple_outputs) == {"gold_region_totals.total_amount", "gold_customer_ltv.lifetime_value"}, "both dependents"  # => co-19
    print(f"MATCH: {target_output!r} traces to exactly {feeding_inputs}, and its source column feeds 2 distinct outputs")  # => co-19
    # => co-19: column-level lineage is what lets a data engineer answer "if I rename this column, which reports break" precisely
