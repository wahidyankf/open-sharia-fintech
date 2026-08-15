---
title: "Capstone artifact: Control mapping"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

This mapping uses NIST CSF 2.0 as an outcome vocabulary. It is a teaching artifact, not an official
implementation profile or an assertion that any control fully satisfies a framework outcome.

| Control                                             | Risks      | CSF outcome area                                                              | Owner                 | Evidence                                               |
| --------------------------------------------------- | ---------- | ----------------------------------------------------------------------------- | --------------------- | ------------------------------------------------------ |
| C-01: authorized, five-minute download grants       | R-01       | Protect: access to customer content is restricted                             | Engineering director  | Quarterly authorization sample and access exceptions   |
| C-02: download-event review and alert investigation | R-01, R-03 | Detect and Respond: suspicious activity is identified and acted on            | Platform lead         | Alert tickets, review record, response notes           |
| C-03: restore exercise against approved targets     | R-02       | Recover: recovery plans and restoration outcomes are tested                   | Platform lead         | Test plan, elapsed recovery result, corrective actions |
| C-04: supplier reassessment and exit decision       | R-04       | Govern and Identify: supplier risk is directed and understood                 | Operations lead       | Assessment, contract review, contingency record        |
| C-05: quarantine and file-verdict handling          | R-03       | Protect, Detect, and Respond: harmful content is constrained and investigated | Product security lead | Verdict log, quarantine record, incident follow-up     |

**Verify forward**: each control has an owner and a contemporaneous evidence item. **Verify
backward**: every listed risk in the risk register has at least one treatment control. If a new risk
is added, the mapping must be reviewed rather than assuming an existing control covers it.

**Assurance decision**: C-03's restore evidence must show whether R-02's 2-hour target is met. If it
is not, the COO receives the residual risk and a funding or acceptance decision.
