---
title: "Artifact: Scoped vs. Open-Ended Prompt -- the Cost Comparison"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 72
---

> The same bug fix, prompted two ways, compared by token cost -- exercises co-18.

| Prompt style                                                                            | Task         | Turns | Total tokens | Total cost |
| --------------------------------------------------------------------------------------- | ------------ | ----- | ------------ | ---------- |
| Open-ended: "the retry logic is flaky, fix it"                                          | same bug fix | 6     | 48,200       | $0.72      |
| Scoped: names `carrier_adapter/retry.py`, the failing assertion, and the fix constraint | same bug fix | 2     | 11,400       | $0.17      |

The open-ended prompt spent its first three turns locating the flaky test, reading the retry module,
and forming a hypothesis before making any change -- work the scoped prompt's author had already
done and simply stated up front.
