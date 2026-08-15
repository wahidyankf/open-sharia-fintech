---
title: "Capstone Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

> **Safe lab boundary.** This capstone consumes only the bundled synthetic event file. It neither
> accepts a target nor starts a network service.

## Goal

Build a reviewable blue-team trail from original lab telemetry: normalize it, validate portable
detections, map coverage, run an incident tabletop, and name hardening follow-up. The goal is a
decision record, not a claim that the toy data represents a production intrusion.

## 1. Verify the local evidence

```sh
# => Verifies the fixture and its expected two alerts without reading a network interface.
sh ../code/check-lab.sh
```

The expected result includes a failed-login-burst decision, a suspicious-request-evidence decision,
and a statement that the single benign failure remains below the threshold.

## 2. Inspect the portable detection

Read [failed-login-burst.yml](../code/failed-login-burst.yml). Identify its `logsource`,
`detection`, and `condition`, then run `python3 ../code/blue_lab.py detect`. Document the
false-positive assumption: a single mistyped password is normal, while three failed attempts from one
synthetic source require review.

## 3. Hunt and map coverage

Run `python3 ../code/blue_lab.py hunt` followed by `python3 ../code/blue_lab.py coverage`.
Record the two teaching mappings and one coverage-gap rule: every authorized red-team lab finding must
have both a detection and remediation before purple-team closure.

## 4. Tabletop and harden

Run `python3 ../code/blue_lab.py tabletop` and complete [ir-report.md](./ir-report.md). Then run
`python3 ../code/blue_lab.py hardening` and assign an owner and verification date to each
reduced-exposure change.

## Acceptance criteria

- The telemetry, detections, and hunt run locally over original synthetic data.
- Each alert has a defensible threshold and a documented false-positive assumption.
- The report covers detect/analyze, contain, eradicate, recover, and lessons learned while noting
  the current NIST Rev. 3 CSF 2.0 context.
- The closeout maps each modeled finding to a detection and a hardening action.
