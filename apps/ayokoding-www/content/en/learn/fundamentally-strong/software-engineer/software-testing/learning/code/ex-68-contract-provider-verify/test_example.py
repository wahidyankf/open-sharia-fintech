"""Example 68: Verify a Small Provider App Against the Pact Produced in Example 67."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

import threading  # => co-24: runs the REAL provider server in the background, in-process  # fmt: skip
import time  # => co-24: polls uvicorn's readiness flag rather than guessing a sleep duration  # fmt: skip
from pathlib import Path  # => types the real pact file path  # fmt: skip

import uvicorn  # => co-24: a REAL ASGI server -- the provider genuinely listens on a socket  # fmt: skip
from pact import Verifier  # => co-24: verifies a REAL running provider against a REAL pact file  # fmt: skip
from provider_app import app  # => the tiny REAL provider from provider_app.py, run for real below  # fmt: skip


def test_provider_satisfies_the_recorded_contract() -> None:  # => co-24: the ONE test in this file  # fmt: skip
    config = uvicorn.Config(app, host="127.0.0.1", port=8199, log_level="warning")  # => a REAL server  # fmt: skip
    server = uvicorn.Server(config)  # => co-24: a REAL uvicorn server instance, not a mock  # fmt: skip
    thread = threading.Thread(
        target=server.run, daemon=True
    )  # => co-24: the provider runs FOR REAL
    thread.start()  # => co-24: a genuine ASGI server, listening on a genuine socket  # fmt: skip
    while not server.started:  # => waits for uvicorn's OWN readiness flag, not a guessed sleep()  # fmt: skip
        time.sleep(0.05)  # => co-24: polls until the REAL server confirms it is listening  # fmt: skip

    try:  # => wrapped so the server always shuts down, pass or fail  # fmt: skip
        pact_file = (
            Path(__file__).parent
            / "pacts"
            / "storefront-consumer-catalog-provider.json"
        )  # => real path
        # => the EXACT file Example 67's consumer test captured -- copied here unmodified (co-24)
        assert pact_file.exists()  # => confirms this test is verifying against a REAL captured file  # fmt: skip

        verifier = Verifier(
            "catalog-provider", host="127.0.0.1"
        )  # => MUST match the pact's provider name
        verifier.add_transport(url="http://127.0.0.1:8199")  # => where the REAL provider is listening  # fmt: skip
        verifier.add_source(pact_file)  # => co-24: the CONTRACT this provider must satisfy  # fmt: skip
        verifier.state_handler(lambda: None)  # => co-24: a no-op setup, since _ITEMS is already seeded  # fmt: skip
        verifier.verify()  # => co-24: sends the pact's REAL recorded request to the REAL provider,  # fmt: skip
        # => and compares the REAL response against what Example 67's consumer required
        print("provider verified: the real, running app satisfies the recorded contract")  # => genuine result  # fmt: skip
    finally:  # => runs whether verify() passed or raised  # fmt: skip
        server.should_exit = True  # => signals uvicorn's OWN clean-shutdown path  # fmt: skip
        thread.join(timeout=5)  # => waits for the real server thread to actually stop  # fmt: skip
