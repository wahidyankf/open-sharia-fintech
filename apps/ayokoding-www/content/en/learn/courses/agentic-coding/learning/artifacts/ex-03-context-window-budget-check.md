---
title: "Artifact: Context-Window Budget Report"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 43
---

> A session's reported context usage (files loaded, token count) checked against the harness's
> documented context limit -- exercises co-03.

| File loaded                     | Tokens | Running total |
| ------------------------------- | ------ | ------------- |
| `src/orders/checkout.py`        | 420    | 420           |
| `src/orders/calculate_total.py` | 180    | 600           |
| `tests/test_checkout.py`        | 610    | 1,210         |
| `README.md`                     | 1,150  | 2,360         |
| `CHANGELOG.md`                  | 3,200  | 5,560         |

Documented context-window ceiling for this session's harness: **200,000 tokens** (stated in the
harness's own session-configuration report). After loading all five files, the session's own
reported running total is 5,560 tokens -- roughly 2.8% of that ceiling.

**Verify**: the reported running total (5,560) is checked directly against the harness's
documented context-window limit (200,000), confirming ample headroom rather than an unexamined
number -- satisfying ex-03's rule of checking the reported count against the documented limit.
