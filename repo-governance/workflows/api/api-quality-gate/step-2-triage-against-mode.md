---
description: How AET findings' ISTQB severity ratings map onto the gate's CRITICAL/HIGH/MEDIUM/LOW mode threshold.
when_to_use: Use when deciding which discovery findings require the bounded fix and verification path.
---

# Step 2: Triage Against Mode

Filter findings by the `mode` threshold. Findings below the threshold are reported but do not block
termination.

If no finding remains in threshold, finalize with `pass`. Otherwise preserve the original finding
IDs and reproduction steps as the complete verification target, then continue to Step 3.

`api-exploratory-tester` rates findings on the **ISTQB severity scale** (Blocker / Critical / Major /
Minor / Trivial), which is not the CRITICAL/HIGH/MEDIUM/LOW vocabulary the `mode` input names. Map
severity to threshold as follows — Priority is a separate axis and never substitutes for severity:

| `mode`   | In-threshold ISTQB severities            | Equivalent named level |
| -------- | ---------------------------------------- | ---------------------- |
| `lax`    | Blocker, Critical                        | CRITICAL only          |
| `normal` | Blocker, Critical, Major                 | CRITICAL + HIGH        |
| `strict` | Blocker, Critical, Major, Minor          | + MEDIUM               |
| `ocd`    | Blocker, Critical, Major, Minor, Trivial | all levels             |
