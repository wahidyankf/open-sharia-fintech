# Runnable example mapping

Every level-page command invokes `cdp_simulation.py` with its named scenario. The artifact is
standard-library-only and runs locally with `python3 cdp_simulation.py <scenario>`; it intentionally
does not launch Chrome, open a WebSocket, or contact a website. This is the safe simulation boundary
for lessons whose real action would require an authorized browser fixture.

The artifact has line-by-line `# =>` annotations: command construction, event-loop yield, response-id
correlation, and deterministic JSON output. Each example maps one-to-one to the scenario shown in its
**Code** line and validates the same observable contract: a correlated response with `safe: true`.

To adapt an example to real CDP, replace `simulate` with a local, authorized transport adapter while
keeping the command id, deadline, allowlist, and observable assertion intact.
