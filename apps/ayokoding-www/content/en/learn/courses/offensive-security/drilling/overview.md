---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## 1. Recall: state the engagement gate

Name the four facts that must be recorded before any test: owner authorization, in-scope local target,
out-of-scope boundaries, and a stop/contact condition. Explain why a target being publicly reachable
does not make it authorized.

## 2. Judgment: reject an unsafe request

A colleague asks you to "quickly check" a customer domain with no written permission. Decline it,
state what is missing, and offer to use the synthetic local fixture instead. Identify the difference
between an observation in a self-owned lab and a test against a third-party system.

## 3. Code: validate a local-only scope

Run `sh ../learning/code/check_scope.sh`. Change the fixture's target from `localhost` to an external
hostname and confirm the script refuses it. Do not replace the fixture with a real target; the point is
to prove a safety guard fails closed.

## 4. Transfer: turn evidence into a finding

Read the supplied local JSON evidence. Write a finding with a short reproduction description,
business impact, a CVSS-style rationale, and one concrete remediation. Keep names, data, and systems
synthetic; do not collect evidence from a live target.

## 5. Self-check: close the lab cleanly

Before sharing a report, ask: is every target self-owned and authorized, is each claim backed by
local evidence, did the report avoid secrets, and does each finding name a remediation? If any answer
is no, stop and correct the report before proceeding.
