"""Example 80: Capstone Preview - License and CAP Rationale."""  # => co-03,co-04,co-28: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-28: a typed rationale entry, one per store the capstone will use


@dataclass(frozen=True)  # => frozen -- a rationale is a stated, citable conclusion, matching Example 67's own pattern
class StoreRationale:  # => co-03,co-04,co-28: the exact 3 fields the capstone's own rationale.md must state per store
    store: str  # => which store this rationale is about
    access_pattern: str  # => co-08: the access pattern that JUSTIFIES choosing this store
    cap_pacelc_position: str  # => co-03,co-04: this store's own CAP/PACELC classification
    license_name: str  # => co-28: the EXACT, checked license name -- never a vague "open source" claim


# The capstone's own 3 stores, previewed here -- the SAME rationale shape drafts_a full page for
# `learning/capstone/rationale.md` (co-03, co-04, co-28).
CAPSTONE_RATIONALES = [  # => co-03,co-04,co-28: one rationale entry per capstone store
    StoreRationale(  # => rationale 1 -- Valkey, the capstone's own session/cache tier
        store="Valkey (session/cache store, kv.py)",  # => the SPECIFIC capstone module this rationale is scoped to
        access_pattern="TTL-bound session tokens, single-key CRUD, disposable by design (co-20, co-24)",  # => the access pattern that JUSTIFIES this store's choice
        cap_pacelc_position="AP/PA/EL -- a single-node cache favors availability and low latency over strict consistency",  # => this store's own CAP/PACELC commitment
        license_name="BSD-3-Clause (Valkey, the Linux Foundation fork, per Example 25's own citation)",  # => the EXACT, checked license name, cited back to its source
    ),  # => closes rationale 1's StoreRationale(...) call
    StoreRationale(  # => rationale 2 -- MongoDB, the capstone's own document tier
        store="MongoDB (document store, doc.py)",  # => a DIFFERENT capstone module, its own independently-justified position
        access_pattern="product-with-stock-level and category-sorted-by-price, both index-served (co-08, co-17)",  # => the access pattern that JUSTIFIES this store's choice
        cap_pacelc_position="CP/PC/EC -- a majority write concern favors consistency over availability under partition",  # => this store's own CAP/PACELC commitment
        license_name="SSPLv1, NOT OSI-approved open source (per Example 26's own citation)",  # => the EXACT, checked license name -- deliberately NOT glossed over
    ),  # => closes rationale 2's StoreRationale(...) call
    StoreRationale(  # => rationale 3 -- Cassandra, the capstone's own wide-column tier
        store="Cassandra (wide-column store, wide.py)",  # => the THIRD capstone module, its own independently-justified position
        access_pattern="order history per customer, an append-heavy, partition-scoped feed (co-22, co-25)",  # => the access pattern that JUSTIFIES this store's choice
        cap_pacelc_position="AP/PA/EL at ONE, or CP/PC/EC at QUORUM -- tunable per query (co-07)",  # => this store's own CAP/PACELC commitment, tunable rather than fixed
        license_name="Apache License 2.0, Apache Software Foundation top-level project (per Example 27's own citation)",  # => the EXACT, checked license name, cited back to its source
    ),  # => closes rationale 3's StoreRationale(...) call
]  # => closes CAPSTONE_RATIONALES -- exactly 3 entries, one per capstone module


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for rationale in CAPSTONE_RATIONALES:  # => co-03,co-04,co-28: prints and verifies every rationale
        print(f"{rationale.store}")  # => Output line -- the store this rationale is about
        print(f"  Access pattern: {rationale.access_pattern}")  # => Output line -- co-08's own justification
        print(f"  CAP/PACELC:     {rationale.cap_pacelc_position}")  # => Output line -- co-03/co-04's own classification
        print(f"  License:        {rationale.license_name}")  # => Output line -- co-28's own checked citation
        assert rationale.access_pattern != ""  # => co-08: every choice is JUSTIFIED by a stated access pattern, never left blank
        assert "/" in rationale.cap_pacelc_position  # => co-03,co-04: every store commits to an explicit CAP/PACELC position
        assert rationale.license_name != ""  # => co-28: every store's license is NAMED, never merely assumed
    assert len(CAPSTONE_RATIONALES) == 3  # => co-28: exactly 3 rationales -- one per capstone store, matching kv.py/doc.py/wide.py
    print(f"All {len(CAPSTONE_RATIONALES)} store rationales drafted -- this IS the content the capstone's rationale.md will formalize")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
