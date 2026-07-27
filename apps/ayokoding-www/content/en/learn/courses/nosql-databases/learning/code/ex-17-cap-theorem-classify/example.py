"""Example 17: Classify by CAP Theorem."""  # => co-03: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from enum import Enum, auto  # => co-03: CP/AP as a checkable type, not a bare string


class CapLean(Enum):  # => co-03: under a network partition, a store leans toward ONE of these two, never both
    CP = auto()  # => co-03: Consistent + Partition-tolerant -- refuses a request rather than risk stale data
    AP = auto()  # => co-03: Available + Partition-tolerant -- answers anyway, possibly with stale data


CONFIGURED_LEAN: dict[str, CapLean] = {  # => co-03: the reference answer key for three SPECIFICALLY configured stores
    "MongoDB (default replica set, majority write concern)": CapLean.CP,  # => co-03: a partitioned-away primary steps down, refusing writes
    "Cassandra (QUORUM read + QUORUM write)": CapLean.CP,  # => co-03: quorum overlap guarantees the read sees the latest write
    "DynamoDB (default eventually-consistent reads)": CapLean.AP,  # => co-03: answers from whichever replica is reachable, possibly stale
}  # => co-03: 3 SPECIFIC configurations, not 3 products -- the SAME product can appear under either lean


def classify_cap(store_config: str) -> CapLean:  # => a pure lookup against the documented guarantee for that config
    """Return the CAP lean for one SPECIFICALLY configured store."""  # => documents the contract, no runtime output
    return CONFIGURED_LEAN[store_config]  # => co-03: KeyError on an unrecognized config -- CAP lean is config-specific, never guessed


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for config, expected in CONFIGURED_LEAN.items():  # => co-03: verifies every entry in the reference answer key
        actual = classify_cap(config)  # => runs the classification for this one configuration
        assert actual == expected  # => co-03: the lookup must agree with itself -- a sanity check on the table
        print(f"{config}: {actual.name}")  # => Output (one line per config): ... : CP / ... : CP / ... : AP
    print("CAP theorem note: the SAME product can lean CP or AP depending on how it is configured")  # => Output: CAP theorem note: the SAME product can lean CP or AP depending on how it is configured


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
