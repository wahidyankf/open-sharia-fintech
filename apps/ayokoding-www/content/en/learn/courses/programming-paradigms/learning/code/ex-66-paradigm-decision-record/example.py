"""Example 66: Paradigm Decision Record."""

from dataclasses import dataclass  # => @dataclass generates DecisionRow's __init__ from its three fields


@dataclass(frozen=True)  # => one row: a problem shape, the paradigm that fits it, and WHY
class DecisionRow:  # => frozen=True -- a recorded decision is a fact, never edited in place
    problem_shape: str  # => the situation this row applies to
    recommended_paradigm: str  # => the paradigm this row recommends for that situation
    selection_criterion: str  # => a CONCRETE reason, not a vibe -- this is the whole point of a decision record


DECISION_TABLE: list[DecisionRow] = [  # => the whole decision policy STATED as data, not scattered comments
    DecisionRow(  # => row 1: combinatorial search
        "search over a large combinatorial space with declared rules",  # => the problem shape
        "constraint/logic",  # => the recommended paradigm
        "backtracking search is the solver's job, not yours -- see ex-38/ex-39/ex-61",  # => the criterion, with concrete cross-references
    ),  # => closes row 1
    DecisionRow(  # => row 2: synchronized UI state
        "UI state that must stay in sync with many derived values",  # => the problem shape
        "reactive",  # => the recommended paradigm
        "automatic propagation eliminates the 'forgot to update X' bug class -- see ex-42",  # => the criterion
    ),  # => closes row 2
    DecisionRow(  # => row 3: batch transforms
        "batch transformation of a fixed dataset, no shared mutable state",  # => the problem shape
        "functional",  # => the recommended paradigm
        "a pure fold is trivially testable with no I/O and safely parallelizable -- see ex-11/ex-48",  # => the criterion
    ),  # => closes row 3
    DecisionRow(  # => row 4: addressable stateful entities
        "a small number of stateful, addressable entities exchanging messages",  # => the problem shape
        "OO / actor",  # => the recommended paradigm
        "encapsulation localizes the mutable state message-sends act on -- see ex-06/ex-65",  # => the criterion
    ),  # => closes row 4
    DecisionRow(  # => row 5: the "paradigm is noise" case
        "a 15-line one-off script with no reuse or team-scale concerns",  # => the problem shape
        "whichever is fastest to write",  # => the recommended paradigm -- or rather, the absence of a strong one
        "paradigm choice earns its weight only once a system has a dominant axis of change -- see ex-28",  # => the criterion
    ),  # => closes row 5
]  # => closes the decision table -- five rows, each with a concrete, cross-referenced justification

for row in DECISION_TABLE:  # => print every row: the table format itself is part of what's verified
    print(f"{row.problem_shape} -> {row.recommended_paradigm}")  # => selection_criterion drives the choice but isn't printed here
# => Output: search over a large combinatorial space with declared rules -> constraint/logic
# => Output: UI state that must stay in sync with many derived values -> reactive
# => Output: batch transformation of a fixed dataset, no shared mutable state -> functional
# => Output: a small number of stateful, addressable entities exchanging messages -> OO / actor
# => Output: a 15-line one-off script with no reuse or team-scale concerns -> whichever is fastest to write
