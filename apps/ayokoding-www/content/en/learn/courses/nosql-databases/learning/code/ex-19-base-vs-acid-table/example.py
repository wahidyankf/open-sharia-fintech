"""Example 19: BASE vs. ACID Table."""  # => co-05: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-05: one typed row per property, so every attribution is checkable


@dataclass(frozen=True)  # => frozen -- a comparison row is a stated fact, not something later code edits
class ComparisonRow:  # => co-05: one property, contrasted across both models
    property_name: str  # => the dimension being compared, e.g. "durability guarantee"
    acid_position: str  # => how the ACID model treats this property
    base_position: str  # => how the BASE model treats the SAME property


COMPARISON: list[ComparisonRow] = [  # => co-05: the full property-by-property contrast this example verifies
    ComparisonRow("Availability under partition", "may refuse a request (co-03: CP-leaning)", "stays available, may answer stale (co-03: AP-leaning)"),  # => row 1: co-03's own CAP lean, restated
    ComparisonRow("Consistency timing", "immediate -- every committed read sees the latest write", "eventual -- replicas converge over time, not instantly (co-06)"),  # => row 2: WHEN a read reflects the latest write
    ComparisonRow("State model", "committed or not -- no in-between state is ever visible", "soft state -- a value CAN change even with no new write, mid-convergence"),  # => row 3: what "soft state" concretely means
    ComparisonRow("Isolation", "concurrent transactions cannot observe each other's uncommitted state", "not guaranteed -- BASE has no isolation concept at all"),  # => row 4: BASE has NO isolation analogue at all
    ComparisonRow("Typical cost paid for the guarantee", "coordination latency on every write", "occasional stale reads, resolved by convergence or app logic"),  # => row 5: the concrete price each model actually pays
]  # => 5 rows, one per property -- ACID and BASE are named for what each one is willing to sacrifice


def acid_properties() -> set[str]:  # => the properties actually named by A-C-I-D
    """Return the 4 canonical ACID property names."""  # => documents the contract, no runtime output
    return {"Atomicity", "Consistency", "Isolation", "Durability"}  # => co-05: the acronym's own 4 letters


def base_properties() -> set[str]:  # => the properties actually named by B-A-S-E
    """Return the 3 canonical BASE property names."""  # => documents the contract, no runtime output
    return {"Basically Available", "Soft state", "Eventually consistent"}  # => co-05: the acronym's own 3 letters


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    assert len(acid_properties()) == 4  # => co-05: ACID names exactly 4 properties
    assert len(base_properties()) == 3  # => co-05: BASE names exactly 3 properties
    for row in COMPARISON:  # => co-05: prints the full property-by-property table
        print(f"{row.property_name} | ACID: {row.acid_position} | BASE: {row.base_position}")  # => Output (5 lines, one per property)
    assert len(COMPARISON) == 5  # => confirms every property in the table above was actually printed
    print("5 properties compared: BASE trades ACID's immediate guarantees for availability and speed")  # => Output: 5 properties compared: BASE trades ACID's immediate guarantees for availability and speed


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
