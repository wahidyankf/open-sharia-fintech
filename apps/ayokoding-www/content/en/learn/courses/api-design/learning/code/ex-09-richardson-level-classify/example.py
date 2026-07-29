# pyright: strict
"""Example 9: Classify Three APIs by Richardson Maturity Model Level. (co-04)

The RMM ladder -- L0 POX, L1 resources, L2 HTTP verbs+status, L3 hypermedia
-- gauges how "RESTful" an API actually is. This example scores three small,
self-described sample APIs against the ladder's own criteria.
"""

from dataclasses import dataclass  # => a small typed record for each sample API's own profile


@dataclass  # => the four yes/no facts the RMM ladder is scored from
class ApiProfile:  # => co-04: one sample API's own self-reported RMM facts
    name: str  # => a human label for this sample API
    has_resource_uris: bool  # => L1: does the URI name a resource, not one single RPC endpoint?
    uses_http_verbs_and_status: bool  # => L2: do distinct methods/status codes carry meaning?
    includes_hypermedia_links: bool  # => L3: does a response include links to next actions?


def rmm_level(api: ApiProfile) -> int:  # => co-04: walks the ladder from the top down
    if api.includes_hypermedia_links:  # => L3 requires L1+L2 to already hold, by construction here
        return 3  # => co-04: Fielding's true REST -- the ladder's top rung
    if api.uses_http_verbs_and_status:  # => L2: distinct verbs/status codes, but no hypermedia
        return 2  # => co-04: HTTP-idiomatic, but a client must still hardcode every next URL
    if api.has_resource_uris:  # => L1: resource URIs, but one verb/status for everything
        return 1  # => co-04: nouns in the path, no HTTP-verb discipline yet
    return 0  # => L0: a single "POX" endpoint, no resources, no verb/status meaning


SAMPLES = (  # => three profiles spanning the ladder's bottom, middle, and top
    ApiProfile("Legacy POX", False, False, False),  # => co-04: one /rpc endpoint for everything
    ApiProfile("Basic REST", True, True, False),  # => co-04: resource URIs + real verbs/status
    ApiProfile("Hypermedia API", True, True, True),  # => co-04: adds _links -- Fielding's true REST
)  # => end of the SAMPLES tuple
# => SAMPLES has exactly 3 elements, spanning L0, L2, and L3 (no sample lands on L1)

for api in SAMPLES:  # => classify each of the three
    print(f"{api.name}: L{rmm_level(api)}")  # => Output: three lines, "L0", "L2", "L3"
