# Phase 0 Quality-Gate Filter

Under `harness-compatibility-quality-gate`, consume Step 0's exact `delegated-gate-ids` and
lifecycle evidence before Phase 0. Delegate Invariants 1–4 only where an exact vendor, binding,
ownership, catalog, or duplication ID (or declared `verifies` relationship) owns the predicate.
Do not run the Invariant 3 generator as a check. Retain Invariant 5's unregistered semantic mapping
judgement and Invariant 6's hand-authored config-intent comparison.

Missing, mismatched, or stale delegated evidence is `pending`; never replace it with a local run
or AI imitation. Continue retained Phase 0 checks and Phase 1 web drift independently. Standalone
invocation runs the full invariant inventory.
