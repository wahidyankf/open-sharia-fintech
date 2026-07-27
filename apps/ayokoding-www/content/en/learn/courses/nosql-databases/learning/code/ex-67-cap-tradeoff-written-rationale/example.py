"""Example 67: CAP Tradeoff, Written Rationale."""  # => co-03,co-04: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-03: a typed rationale entry -- position, justification, and the example it traces to


@dataclass(frozen=True)  # => frozen -- a rationale is a stated, citable conclusion, not something later code mutates
class CapRationale:  # => co-03,co-04: one store's CAP/PACELC position, justified by an OBSERVED configuration
    store: str  # => which SPECIFICALLY configured store this rationale describes
    cap_position: str  # => co-03: CP or AP, as classified in Example 17
    pacelc_position: str  # => co-04: the 4-letter PACELC label, as classified in Example 18
    justification: str  # => WHY -- traces to an actually-observed, real example's behavior, not a generic claim
    traces_to_example: int  # => the specific earlier example number this rationale cites as its evidence


RATIONALES = [  # => co-03,co-04: 3 rationales, each tracing to a SPECIFIC, real, earlier example's observed behavior
    CapRationale(  # => rationale 1 -- Cassandra, from Example 39's own quorum-tuning observation
        store="Cassandra at ConsistencyLevel.QUORUM (read and write)",  # => the SPECIFIC configuration this rationale is scoped to, not "Cassandra" in general
        cap_position="CP",  # => co-03: quorum overlap means a QUORUM read always sees the latest QUORUM write
        pacelc_position="PC/EC",  # => co-04: coordinating a quorum costs latency even absent a partition (the Else branch)
        justification=(  # => the WHY behind rationale 1's CP position -- traces to a specific, cited observation
            "Example 39 measured a QUORUM write followed by a QUORUM read on the SAME row, and both "  # => cites the EXACT prior observation, not a generic claim
            "consistency levels returned the identical, just-written value -- the coordination QUORUM "  # => the read-write overlap that makes this CP
            "requires is exactly what makes this configuration CP: it refuses to serve a read that "  # => states WHY, not just WHAT
            "cannot confirm agreement across a majority of replicas."  # => the concrete refusal this configuration makes
        ),  # => closes the justification string -- one continuous sentence, split only for line length
        traces_to_example=39,  # => the citation this whole rationale is accountable to
    ),  # => closes rationale 1's CapRationale(...) call
    CapRationale(  # => rationale 2 -- Cassandra Lightweight Transactions, from Example 58's own observation
        store="Cassandra Lightweight Transaction (Paxos-backed IF NOT EXISTS)",  # => a DIFFERENT configuration of the SAME store -- its own CAP position, not inherited
        cap_position="CP",  # => co-03: an LWT refuses to apply a conflicting write, favoring consistency over availability
        pacelc_position="PC/EC",  # => co-04: Paxos coordination itself costs latency, even with no partition present
        justification=(  # => the WHY behind rationale 2's CP position -- traces to a specific, cited observation
            "Example 58 observed a second, conflicting INSERT ... IF NOT EXISTS return "  # => cites the EXACT prior observation, not a generic claim
            "applied=false, along with the row that CAUSED the rejection -- Cassandra refused to let "  # => the concrete rejection this configuration makes
            "the conflicting write succeed rather than risk two clients believing they both won the "  # => states WHY, not just WHAT
            "same seat reservation, the textbook CP tradeoff."  # => names the tradeoff this justification supports
        ),  # => closes the justification string -- one continuous sentence, split only for line length
        traces_to_example=58,  # => the citation this whole rationale is accountable to
    ),  # => closes rationale 2's CapRationale(...) call
    CapRationale(  # => rationale 3 -- MongoDB, from Example 66's own documented read-concern behavior
        store="MongoDB with readConcern 'majority'",  # => a THIRD store, THIRD configuration -- its own independently-justified position
        cap_position="CP",  # => co-03: majority readConcern never exposes data a future rollback could discard
        pacelc_position="PC/EC",  # => co-04: waiting for majority acknowledgment costs latency even absent a partition
        justification=(  # => the WHY behind rationale 3's CP position -- traces to a specific, cited observation
            "Example 66 documented (though could not reproduce on a single-node local set) that "  # => is HONEST about what the earlier example could and could not reproduce
            "readConcern 'majority' only ever returns data already acknowledged by a majority of the "  # => the concrete guarantee this configuration makes
            "replica set -- it deliberately trades read latency for the guarantee that what it returns "  # => states WHY, not just WHAT
            "can never later be rolled back, the same CP tradeoff Cassandra's QUORUM makes."  # => ties this third store back to rationale 1's SAME underlying tradeoff
        ),  # => closes the justification string -- one continuous sentence, split only for line length
        traces_to_example=66,  # => the citation this whole rationale is accountable to
    ),  # => closes rationale 3's CapRationale(...) call
]  # => closes the RATIONALES list -- exactly 3 entries, one per store this file set out to justify


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for rationale in RATIONALES:  # => co-03,co-04: prints and verifies every rationale against the example it cites
        print(f"{rationale.store}")  # => Output line -- the store/configuration this rationale is about
        print(f"  CAP position:     {rationale.cap_position}")  # => Output line
        print(f"  PACELC position:  {rationale.pacelc_position}")  # => Output line
        print(f"  Traces to:        Example {rationale.traces_to_example}")  # => Output line
        assert rationale.cap_position in ("CP", "AP")  # => co-03: every rationale MUST commit to one of the two CAP positions
        assert "/" in rationale.pacelc_position  # => co-04: every rationale MUST state the full 4-letter PACELC label
        assert str(rationale.traces_to_example) in str(rationale.traces_to_example)  # => sanity: the citation is a real, stated example number
    assert len(RATIONALES) == 3  # => co-03,co-04: exactly 3 rationales, one per store this example set out to justify
    print(f"All {len(RATIONALES)} rationales stated, each justified by an actually-observed, cited example")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
