# pyright: strict
"""Example 69: Picking a Style per Scenario, with a Rationale. (co-27)

Choosing REST, GraphQL, or gRPC is a design decision, not a default -- this
example encodes a small decision matrix, one scenario per row, and asserts
every recommended style is backed by an explicit, checkable rationale.
"""

from dataclasses import dataclass  # => a small typed record for one scenario's own recommendation


@dataclass  # => co-27: one row -- a scenario, its recommended style, and WHY
class StyleRecommendation:  # => co-27: three fields, one row per scenario in the matrix below
    scenario: str  # => a short description of the situation being decided
    recommended_style: str  # => co-27: REST, GraphQL, or gRPC
    rationale: str  # => co-27: the SPECIFIC property that drove this choice


DECISION_MATRIX = [  # => co-27: a small, explicit table -- not a vague "it depends"
    StyleRecommendation(  # => scenario 1: a public, cacheable, browsable API
        scenario="public API consumed by many unknown third-party clients",  # => scenario 1's own description
        recommended_style="REST",  # => co-27: broad tooling support, HTTP caching (Example 67)
        rationale="cacheable over plain HTTP, universally understood, easy to document (Example 79)",  # => co-27
    ),  # => end of scenario 1
    StyleRecommendation(  # => scenario 2: a mobile client with variable network conditions
        scenario="mobile client on a slow network, many different screens with different data needs",  # => scenario 2
        recommended_style="GraphQL",  # => co-27: avoids Example 59's over-fetching
        rationale="each screen selects exactly its own fields (Example 58), minimizing payload size",  # => co-27
    ),  # => end of scenario 2
    StyleRecommendation(  # => scenario 3: two internal microservices talking to each other
        scenario="two internal microservices exchanging high-volume, low-latency calls",  # => scenario 3's own description
        recommended_style="gRPC",  # => co-27: binary framing, streaming (Examples 64-66)
        rationale="binary Protobuf encoding plus HTTP/2 streaming outperforms JSON-over-HTTP/1.1",  # => co-27
    ),  # => end of scenario 3
]  # => end of DECISION_MATRIX
# => DECISION_MATRIX has exactly 3 rows, one per style this course covers -- no scenario is left vague

VALID_STYLES = {"REST", "GraphQL", "gRPC"}  # => co-27: the only three styles this course covers

for recommendation in DECISION_MATRIX:  # => co-27: verify every row before trusting it
    assert recommendation.recommended_style in VALID_STYLES, "unrecognized style"  # => a real style, not a typo
    assert len(recommendation.rationale) > 0, "every recommendation needs a stated reason"  # => never unjustified
    print(f"{recommendation.scenario!r} -> {recommendation.recommended_style} ({recommendation.rationale})")
    # => Output: three lines, each scenario paired with its style AND its specific justification
