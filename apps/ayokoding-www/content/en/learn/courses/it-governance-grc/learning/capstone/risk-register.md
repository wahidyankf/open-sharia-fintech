---
title: "Capstone artifact: Risk register"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

Northstar Notes' fictional attachment-service register uses the five-point likelihood and impact
scale from Worked Scenario 4. Scores express comparative judgment, not a promise of precision.

| ID   | Risk statement                                                              | Inherent | Treatment and owner                                                                                                     | Residual | Review                                                |
| ---- | --------------------------------------------------------------------------- | -------: | ----------------------------------------------------------------------------------------------------------------------- | -------: | ----------------------------------------------------- |
| R-01 | A guessed or over-shared link could disclose a customer's attachment.       |       15 | Mitigate: authorized, time-bounded downloads and review of access logs. Owner: Engineering director.                    |        6 | Monthly and after any disclosure event.               |
| R-02 | Storage outage could prevent customers from retrieving contractual records. |       12 | Mitigate: tested restore process against business targets. Owner: Platform lead.                                        |        8 | Quarterly restore test and after architecture change. |
| R-03 | A malicious attachment could harm a downloader or service operation.        |       12 | Avoid executable formats; mitigate other formats with scanning, quarantine, and alerting. Owner: Product security lead. |        6 | Monthly plus after detection failure.                 |
| R-04 | A high-tier storage supplier could fail or mishandle attachment data.       |       10 | Mitigate: contract review, supplier reassessment, resilience review, and exit exercise. Owner: Operations lead.         |        6 | Annually and after material supplier change.          |

**Verify**: each row states an asset-facing consequence, inherent and residual ratings, treatment,
one accountable owner, and a specific review trigger. R-02 remains visible at residual 8; a backup
exists, but the critical recovery target has not yet been met.

**Assurance decision**: the COO must decide whether to fund recovery improvements for R-02 before
accepting the residual risk for another quarter. The register does not make that business decision
on the COO's behalf.
