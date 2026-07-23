---
title: "Artifact: Subagent Delegation -- Only the Summary Returns"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 61
---

> A subagent dispatch whose raw exploration stays withheld from the main session -- exercises co-10.

```text
[main session] -> dispatch subagent(
  task: "find where the ParcelLink retry backoff is implemented and summarize the pattern"
)

[subagent, isolated context -- 12 tool calls: 8 file reads, 3 greps, 1 doc search --
 WITHHELD from the main session's context, per co-10]

[subagent -> main session, summary only]:
"CarrierAdapter.get_status() (carrier_adapter/retry.py:14-31) retries a failed ParcelLink
call up to 3 times with exponential backoff (200ms/400ms/800ms) on HTTP 503. No other call
site in the repo implements retry logic independently -- this is the only retry
implementation."
```
