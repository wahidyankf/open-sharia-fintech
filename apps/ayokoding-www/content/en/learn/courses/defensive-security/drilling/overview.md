---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## 1. Recall: trace the defensive loop

State the order synthetic telemetry follows in this course: collect, normalize, detect, investigate,
contain, recover, improve. Name the three structural parts of the course's Sigma rule and explain why
a technique mapping is an organizing label rather than proof of an incident.

## 2. Judgment: tune without hiding risk

The fixture has one ordinary failed login and a burst of three from one source. Explain why a threshold
of one would create noise, then name the evidence you would collect before raising the threshold again.
State when you would stop and involve the service owner.

## 3. Code: validate the local lab

Run `sh ../learning/code/check-lab.sh`. Confirm it prints two reviewable alerts and no network target.
Read `lab-events.ndjson` and change nothing: the drill is to verify a reproducible baseline, not to
replace it with production telemetry.

## 4. Transfer: write a response decision

Use the capstone report template to describe containment, eradication, recovery, and follow-up for the
fictional alert. Include an owner, a required evidence reference, and one hardening action. Keep the
account, service, and source address synthetic.

## 5. Self-check: close the purple-team loop

Before calling an authorized finding closed, ask: is the telemetry retained, is the detection tested
against benign and suspicious fixtures, is the technique mapping recorded, is the response decision
owned, and is the remediation verified? If any answer is no, the coverage gap remains open.
