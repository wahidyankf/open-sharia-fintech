"""Example 38: Quorum Read/Write Math."""  # => co-07: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-07: a typed record for one (N, W, R) configuration


@dataclass(frozen=True)  # => frozen -- a configuration is a stated fact, not something later code mutates
class QuorumConfig:  # => co-07: the 3 tunable knobs behind Cassandra's/Dynamo-style tunable consistency
    label: str  # => a human-readable name for this configuration
    n: int  # => co-07: N -- the total number of replicas holding this data
    w: int  # => co-07: W -- how many replicas must ack a WRITE before it is considered successful
    r: int  # => co-07: R -- how many replicas a READ must consult before returning a result


def guarantees_strong_consistency(config: QuorumConfig) -> bool:  # => co-07: the classic W + R > N overlap condition
    """Return True if W + R > N, guaranteeing the read and write sets overlap by at least one replica."""  # => documents contract
    return config.w + config.r > config.n  # => co-07: overlap guarantees the read set includes at least one replica holding the latest write


CONFIGURATIONS = [  # => co-07: 3 configurations spanning "does not overlap" to "always overlaps"
    QuorumConfig("weak (N=3, W=1, R=1)", n=3, w=1, r=1),  # => 1+1=2, NOT > 3 -- read and write sets can miss each other entirely
    QuorumConfig("classic quorum (N=3, W=2, R=2)", n=3, w=2, r=2),  # => 2+2=4, > 3 -- guaranteed overlap, the standard "QUORUM" setting
    QuorumConfig("write-all, read-one (N=3, W=3, R=1)", n=3, w=3, r=1),  # => 3+1=4, > 3 -- also guaranteed, but W=3 blocks on EVERY replica
]  # => 3 configs, same N=3 -- only the W/R split changes whether overlap is guaranteed


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for config in CONFIGURATIONS:  # => co-07: evaluates the SAME overlap condition against every configuration
        strong = guarantees_strong_consistency(config)  # => runs the W + R > N check for this one configuration
        print(f"{config.label}: W+R={config.w + config.r}, N={config.n}, strongly consistent = {strong}")  # => Output line, one per config
    assert guarantees_strong_consistency(CONFIGURATIONS[0]) is False  # => co-07: W=1,R=1 on N=3 can genuinely miss the latest write
    assert guarantees_strong_consistency(CONFIGURATIONS[1]) is True  # => co-07: the standard QUORUM/QUORUM setting always overlaps
    assert guarantees_strong_consistency(CONFIGURATIONS[2]) is True  # => co-07: overlap holds, but at the cost of blocking on ALL replicas to write
    print("Only configurations where W + R > N guarantee the read observes the latest committed write")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
