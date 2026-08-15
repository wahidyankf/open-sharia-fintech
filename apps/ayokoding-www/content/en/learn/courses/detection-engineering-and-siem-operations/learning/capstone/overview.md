---
title: "Capstone Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

> **Safe lab boundary.** This capstone validates the bundle's original, synthetic files. It accepts no
> target and starts no service. A Wazuh owner may separately review and adapt the concepts in an isolated,
> self-owned lab; this page is never a production deployment guide.

## Goal

Build and defend a compact detection pack for one invented log source: author a Wazuh-style decoder,
base and correlation rules, a dashboard plan, and a false-positive decision record. Prove the entire pack
works against the bundled fictional corpus, including a retained sequence test and a benign case that stays
quiet.

## 1. Verify the local pack

```sh
# => Validates original files and synthetic data; this command opens no socket.
sh ../code/check-lab.sh
```

The result must name the decoder contract, one bounded correlation source, the local dashboard-plan
questions, the `0.25` teaching false-positive rate for the loose base rule, and the retained signal under
the tuned correlation threshold.

## 2. Review decoder and rules as code

Read [local_decoder.xml](../code/local_decoder.xml) and [local_rules.xml](../code/local_rules.xml). The
decoder's `prematch`, `regex`, and `order` form a field contract. The rules then present a base failed
action and a three-events-in-120-seconds, same-source correlation. Explain why each constraint exists and
which local test would fail if you weakened it.

## 3. Build the dashboard question set

Read [dashboard-plan.json](../code/dashboard-plan.json). It defines a severity question, a false-positive
tuning question that preserves the known sequence test, and a tested-coverage question. It is deliberately
a portable planning document, not a copied vendor export or a dashboard to import without review.

## 4. Make the tuning decision

Complete [tuning-record.md](./tuning-record.md) using only the synthetic fixture. Record the loose and
tuned values, the benign denominator, the retained true-positive sequence, an owner, and a review date.
Do not generalize the fixture's numbers to a production service.

## Acceptance criteria

- The decoder extracts the intended fictional fields and rejects an unrelated local line.
- The base rule and same-source correlation have explicit, offline tests.
- The dashboard plan includes false-positive evidence _and_ retained-signal evidence.
- The tuning record names its corpus, assumptions, reviewer, and recheck date.
- The reader can describe the handoff to `defensive-security`'s incident-response practice without
  treating this course as a response or hardening guide.
