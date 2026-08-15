---
title: "Tuning Decision Record"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 2
---

# Synthetic Detection-Pack Tuning Decision

## Evidence scope

- **Corpus**: `learning/code/lab-events.ndjson`, authored only for this course.
- **Rule IDs**: fictional local rules `100500` and `100501`; no claim about a deployed ruleset.
- **Boundary**: this record is a training decision, not a production alert disposition or response order.

## Detection hypothesis

Three fictional failed actions from the same documentation address, followed by a fictional success inside
the stated window, require an analyst to review the bounded evidence. The sequence is a review prompt,
not proof of intent or identity.

## Before and after

| Decision field         | Loose base rule      | Tuned correlation                      | Evidence                     |
| ---------------------- | -------------------- | -------------------------------------- | ---------------------------- |
| Condition              | one `failure` action | three failures + same source + success | `detection_lab.py tune`      |
| Training prompts       | 4                    | 1 correlated source                    | fixed local fixture          |
| Labeled benign prompts | 1                    | 0                                      | fixed local fixture          |
| Retained signal        | not applicable       | `198.51.100.17` sequence               | `detection_lab.py correlate` |

## Assumption and residual risk

The single fictional `lee` failure represents normal retry noise in this tiny corpus. The tuned condition
reduces that labeled noise but could miss a meaningful sequence that does not contain a success or crosses
the chosen window. A production owner must measure its own telemetry and review this trade-off rather than
copying these values.

## Review and follow-up

- **Reviewer**: training detection engineer
- **Owner**: self-owned lab operator
- **Recheck date**: 2026-09-15
- **Regression checks**: `python3 ../code/detection_lab.py verify`
- **Escalation boundary**: if a real owner confirms a true positive, hand response decisions to the
  incident-response process taught in `defensive-security`.
