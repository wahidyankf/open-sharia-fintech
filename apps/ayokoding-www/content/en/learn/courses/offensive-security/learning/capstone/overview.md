---
title: "Local Finding Report"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

> **Authorized lab target only.** This capstone operates on bundled, synthetic `localhost` evidence.
> It must not be pointed at a real-world target, and it sends no network traffic.

## Goal

Produce two concise, remediation-oriented findings from the local fixture. The capstone demonstrates
rules of engagement, evidence interpretation, severity reasoning, and cleanup—not exploitation skill.

## 1. Confirm the rules of engagement

Read [rules-of-engagement.md](./rules-of-engagement.md), then run:

```sh
sh ../code/check_scope.sh
```

The command must say the fixture is an authorized self-owned local lab. If it rejects the fixture,
stop; do not substitute any other host or target.

## 2. Interpret the synthetic evidence

Run `python3 ../code/parse_lab_evidence.py`. It must report one local service and two findings. Read
the data as an owner-provided record, not as a request to probe or verify an external system.

## 3. Write two findings

For `LAB-001` and `LAB-002`, use [report.md](./report.md) to provide:

1. bounded reproduction from the supplied fixture;
2. impact in the fictional training application;
3. a CVSS-style severity rationale; and
4. a concrete remediation plus regression-test idea.

Run `python3 ../code/validate_finding.py` to check the report shape. Do not include credentials,
payloads, copied requests, or sensitive information.

## 4. Close out

Confirm the target was the supplied local fixture, no traffic was sent, no data left the lab, and
the owner-facing report contains remediation. This is the required cleanup record.

## Acceptance criteria

- The authorization and `localhost` boundary are stated before evidence review.
- Two synthetic findings contain reproduction, impact, severity, and remediation.
- Every action stays lab-local and authorized-scope-only.
- No material provides guidance for unauthorized real-world exploitation.
