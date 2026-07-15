"""Example 67: A Pact Consumer Test That Defines the Expected Interaction."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from pathlib import Path  # => types the real, on-disk pact file location  # fmt: skip

import httpx  # => co-24: a REAL HTTP client, requesting the REAL mock server below  # fmt: skip
from pact import Pact  # => co-24: pact-python 3.4.0's PactV3/V4-style consumer API  # fmt: skip


def test_consumer_defines_expected_interaction() -> None:  # => co-24: NO real provider runs here  # fmt: skip
    pact = Pact("storefront-consumer", "catalog-provider")  # => co-24: names BOTH sides of the contract  # fmt: skip
    (  # => co-24: describes the interaction the CONSUMER expects, in full, before any code calls it  # fmt: skip
        pact.upon_receiving(
            "a request for item 1"
        )  # => co-24: names this ONE interaction  # fmt: skip
        .given(
            "item 1 exists"
        )  # => the PROVIDER STATE ex-68's provider must be able to set up  # fmt: skip
        .with_request(
            "GET", "/items/1"
        )  # => the EXACT request this contract governs  # fmt: skip
        .will_respond_with(200)  # => the status the consumer requires  # fmt: skip
        .with_header(
            "Content-Type", "application/json"
        )  # => the header the consumer requires  # fmt: skip
        .with_body(
            {"id": 1, "name": "widget"}
        )  # => the EXACT body shape the consumer requires  # fmt: skip
    )

    with pact.serve() as mock_server:  # => co-24: pact spins up a REAL mock HTTP server FOR THIS TEST  # fmt: skip
        # The consumer's REAL HTTP client code runs against this mock, exactly as it would in prod --
        # this is pact-python genuinely verifying the CONSUMER side matches its own stated contract.
        response = httpx.get(f"{mock_server.url}/items/1")  # => a REAL request, to the REAL mock  # fmt: skip
        assert response.status_code == 200  # => confirms the mock genuinely honored the contract  # fmt: skip
        assert response.json() == {"id": 1, "name": "widget"}  # => confirms the REAL body shape  # fmt: skip

    pacts_dir = Path(__file__).parent / "pacts"  # => co-24: where the CAPTURED contract file lands  # fmt: skip
    pacts_dir.mkdir(exist_ok=True)  # => co-24: creates the REAL directory on disk if needed  # fmt: skip
    pact.write_file(pacts_dir)  # => co-24: writes the interaction ABOVE to a real, on-disk pact file  # fmt: skip
    written = pacts_dir / "storefront-consumer-catalog-provider.json"  # => the REAL file path  # fmt: skip
    assert written.exists()  # => co-24: confirms a real pact FILE, not just an in-memory object  # fmt: skip
    print(
        f"pact file written: {written}"
    )  # => the exact artifact ex-68's provider test verifies against
